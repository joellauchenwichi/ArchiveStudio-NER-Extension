import spacy
from collections import defaultdict
import pandas as pd
from tkinter import messagebox

class EnhancedNERHandler:
    """
    Enhanced NER handler using spaCy to extend Names and Places functionality
    Extracts: PERSON, GPE (locations), ORG, DATE, MONEY, and other entities
    """
    
    def __init__(self, app):
        self.app = app
        self.nlp = None
        self.entity_types = {
            'PERSON': 'People',
            'GPE': 'Places',  # Geopolitical entities (cities, countries)
            'LOC': 'Places',  # Non-GPE locations
            'ORG': 'Organizations',
            'DATE': 'Dates',
            'MONEY': 'Money',
            'EVENT': 'Events',
            'WORK_OF_ART': 'Works',
            'LAW': 'Laws',
            'LANGUAGE': 'Languages',
            'PRODUCT': 'Products'
        }
        self.load_model()
    
    def load_model(self):
        """Load spaCy model (with error handling for missing models)"""
        try:
            # Try to load the model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not installed
            try:
                messagebox.showinfo(
                    "Installing spaCy Model",
                    "First-time setup: Installing spaCy language model.\n"
                    "This may take a moment..."
                )
                import subprocess
                subprocess.check_call([
                    "python", "-m", "spacy", "download", "en_core_web_sm"
                ])
                self.nlp = spacy.load("en_core_web_sm")
                messagebox.showinfo("Success", "spaCy model installed successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to install spaCy model: {e}\n\n"
                    "Please run: python -m spacy download en_core_web_sm"
                )
                self.nlp = None
    
    def extract_entities(self, text, entity_types=None):
        """
        Extract entities from text using spaCy
        
        Args:
            text: Text to analyze
            entity_types: List of entity types to extract (None = all)
        
        Returns:
            dict: {entity_type: [list of entities]}
        """
        if not self.nlp or not text:
            return {}
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Organize entities by type
        entities = defaultdict(set)
        
        for ent in doc.ents:
            # Map spaCy entity type to our categories
            mapped_type = self.entity_types.get(ent.label_, ent.label_)
            
            # Filter by requested types if specified
            if entity_types is None or mapped_type in entity_types:
                entities[mapped_type].add(ent.text.strip())
        
        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in entities.items()}
    
    def process_current_page(self):
        """Extract entities from current page"""
        if self.app.main_df.empty or self.app.page_counter >= len(self.app.main_df):
            messagebox.showwarning("Warning", "No page to process")
            return
        
        index = self.app.page_counter
        text = self.app.data_operations.find_right_text(index)
        
        if not text.strip():
            messagebox.showwarning("Warning", "No text found to analyze")
            return
        
        # Extract entities
        entities = self.extract_entities(text)
        
        # Update DataFrame with extracted entities
        self._update_dataframe_entities(index, entities)
        
        # Show results
        self._show_extraction_results(entities)
    
    def process_all_pages(self):
        """Extract entities from all pages"""
        if self.app.main_df.empty:
            messagebox.showwarning("Warning", "No pages to process")
            return
        
        total = len(self.app.main_df)
        progress_window, progress_bar, progress_label = self.app.progress_bar.create_progress_window("Extracting Entities")
        
        all_entities = defaultdict(set)
        
        for idx, index in enumerate(self.app.main_df.index):
            text = self.app.data_operations.find_right_text(index)
            
            if text.strip():
                entities = self.extract_entities(text)
                
                # Update DataFrame
                self._update_dataframe_entities(index, entities)
                
                # Accumulate all unique entities
                for entity_type, entity_list in entities.items():
                    all_entities[entity_type].update(entity_list)
            
            self.app.progress_bar.update_progress(idx+1, total)
        
        self.app.progress_bar.close_progress_window()
        
        # Convert to sorted lists
        all_entities = {k: sorted(list(v)) for k, v in all_entities.items()}
        
        # Show results
        self._show_extraction_results(all_entities, total_pages=total)
        
        # Refresh display
        self.app.refresh_display()
    
    def _update_dataframe_entities(self, index, entities):
        """Update DataFrame with extracted entities"""
        # Update People and Places (existing columns)
        if 'People' in entities:
            self.app.main_df.at[index, 'People'] = ', '.join(entities['People'])
        
        if 'Places' in entities:
            self.app.main_df.at[index, 'Places'] = ', '.join(entities['Places'])
        
        # Add new columns for other entity types if needed
        for entity_type, entity_list in entities.items():
            if entity_type not in ['People', 'Places']:
                col_name = f'NER_{entity_type}'
                if col_name not in self.app.main_df.columns:
                    self.app.main_df[col_name] = ''
                self.app.main_df.at[index, col_name] = ', '.join(entity_list)
    
    def _show_extraction_results(self, entities, total_pages=1):
        """Display extraction results to user"""
        if not entities:
            messagebox.showinfo("Results", "No entities found")
            return
        
        result_text = f"Entities extracted from {total_pages} page(s):\n\n"
        
        for entity_type, entity_list in sorted(entities.items()):
            result_text += f"{entity_type}: {len(entity_list)} unique\n"
            # Show first few examples
            examples = entity_list[:5]
            result_text += f"  Examples: {', '.join(examples)}"
            if len(entity_list) > 5:
                result_text += f" (+{len(entity_list) - 5} more)"
            result_text += "\n"
        
        messagebox.showinfo("Extraction Complete", result_text)
    
    def export_entities_to_excel(self, output_path):
        """
        Export all entities to Excel in database format
        Creates separate sheets for each entity type
        """
        if self.app.main_df.empty:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        # Collect all entity columns
        entity_columns = ['People', 'Places']
        entity_columns += [col for col in self.app.main_df.columns if col.startswith('NER_')]
        
        # Create Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Create summary sheet
            self._create_summary_sheet(writer, entity_columns)
            
            # Create individual entity sheets
            for col in entity_columns:
                self._create_entity_sheet(writer, col)
            
            # Create master data sheet with all information
            self._create_master_sheet(writer, entity_columns)
        
        messagebox.showinfo("Success", f"Entities exported to:\n{output_path}")
    
    def _create_summary_sheet(self, writer, entity_columns):
        """Create summary statistics sheet"""
        summary_data = []
        
        for col in entity_columns:
            # Count non-empty cells
            non_empty = self.app.main_df[col].notna() & (self.app.main_df[col] != '')
            count = non_empty.sum()
            
            # Count unique entities
            all_entities = set()
            for val in self.app.main_df[col].dropna():
                if val:
                    all_entities.update([e.strip() for e in str(val).split(',')])
            
            summary_data.append({
                'Entity Type': col.replace('NER_', ''),
                'Pages with Entities': count,
                'Unique Entities': len(all_entities),
                'Total Mentions': sum(str(val).count(',') + 1 for val in self.app.main_df[col].dropna() if val)
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    def _create_entity_sheet(self, writer, column_name):
        """Create detailed sheet for specific entity type"""
        entity_data = []
        
        for index, row in self.app.main_df.iterrows():
            entities_str = row.get(column_name, '')
            if pd.notna(entities_str) and entities_str:
                entities = [e.strip() for e in str(entities_str).split(',')]
                page_num = index + 1
                
                for entity in entities:
                    entity_data.append({
                        'Entity': entity,
                        'Page': page_num,
                        'Document_No': row.get('Page', ''),
                        'Context': self._get_context(row, entity)
                    })
        
        if entity_data:
            entity_df = pd.DataFrame(entity_data)
            # Sort by entity name
            entity_df = entity_df.sort_values('Entity')
            sheet_name = column_name.replace('NER_', '')[:31]  # Excel sheet name limit
            entity_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def _create_master_sheet(self, writer, entity_columns):
        """Create master sheet with all data"""
        # Select relevant columns
        export_columns = ['Index', 'Page'] + entity_columns + ['Image_Path']
        
        # Add text columns if they exist
        text_cols = ['Original_Text', 'Corrected_Text', 'Formatted_Text', 'Translation']
        for col in text_cols:
            if col in self.app.main_df.columns:
                export_columns.append(col)
        
        master_df = self.app.main_df[export_columns].copy()
        master_df.to_excel(writer, sheet_name='Master Data', index=False)
    
    def _get_context(self, row, entity, context_chars=100):
        """Get text context around entity"""
        # Try to find entity in available text
        for col in ['Formatted_Text', 'Corrected_Text', 'Original_Text', 'Translation']:
            if col in row and pd.notna(row[col]):
                text = str(row[col])
                pos = text.find(entity)
                if pos != -1:
                    start = max(0, pos - context_chars)
                    end = min(len(text), pos + len(entity) + context_chars)
                    context = text[start:end]
                    if start > 0:
                        context = '...' + context
                    if end < len(text):
                        context = context + '...'
                    return context
        return ''