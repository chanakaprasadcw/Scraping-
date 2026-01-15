"""Data export functionality for leads."""

import os
import json
from datetime import datetime
from typing import List, Dict
import pandas as pd


class DataExporter:
    """Export lead data to various formats."""

    def __init__(self, output_dir: str = './output'):
        """
        Initialize data exporter.

        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_to_csv(self, leads: List[Dict], filename: str = 'leads') -> str:
        """
        Export leads to CSV file.

        Args:
            leads: List of lead dictionaries
            filename: Output filename (without extension)

        Returns:
            Path to exported file
        """
        if not leads:
            print("No leads to export")
            return None

        # Flatten the lead data for CSV
        flattened_leads = []
        for lead in leads:
            flat_lead = {
                'name': lead.get('name', ''),
                'company': lead.get('company', lead.get('current_company', '')),
                'position': lead.get('title', lead.get('current_position', '')),
                'location': lead.get('location', ''),
                'linkedin_url': lead.get('linkedin_url', lead.get('url', '')),
                'emails': ', '.join(lead.get('emails', [])),
                'about': lead.get('about', '')[:200] if lead.get('about') else '',  # Truncate
                'headline': lead.get('headline', ''),
            }

            # Add experience if available
            if lead.get('experience'):
                exp = lead['experience'][0] if isinstance(lead['experience'], list) else {}
                flat_lead['previous_position'] = exp.get('position', '')
                flat_lead['previous_company'] = exp.get('company', '')

            # Add social links
            social_links = lead.get('social_links', {})
            for platform, url in social_links.items():
                flat_lead[f'{platform}_url'] = url

            flattened_leads.append(flat_lead)

        # Create DataFrame
        df = pd.DataFrame(flattened_leads)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(self.output_dir, f'{filename}_{timestamp}.csv')

        # Export to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✅ Exported {len(leads)} leads to: {output_path}")

        return output_path

    def export_to_json(self, leads: List[Dict], filename: str = 'leads') -> str:
        """
        Export leads to JSON file.

        Args:
            leads: List of lead dictionaries
            filename: Output filename (without extension)

        Returns:
            Path to exported file
        """
        if not leads:
            print("No leads to export")
            return None

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(self.output_dir, f'{filename}_{timestamp}.json')

        # Export to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Exported {len(leads)} leads to: {output_path}")

        return output_path

    def export_to_excel(self, leads: List[Dict], filename: str = 'leads') -> str:
        """
        Export leads to Excel file with multiple sheets.

        Args:
            leads: List of lead dictionaries
            filename: Output filename (without extension)

        Returns:
            Path to exported file
        """
        if not leads:
            print("No leads to export")
            return None

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(self.output_dir, f'{filename}_{timestamp}.xlsx')

        # Flatten for main sheet
        flattened_leads = []
        for lead in leads:
            flat_lead = {
                'Name': lead.get('name', ''),
                'Company': lead.get('company', lead.get('current_company', '')),
                'Position': lead.get('title', lead.get('current_position', '')),
                'Location': lead.get('location', ''),
                'LinkedIn URL': lead.get('linkedin_url', lead.get('url', '')),
                'Emails': ', '.join(lead.get('emails', [])),
                'Headline': lead.get('headline', ''),
            }
            flattened_leads.append(flat_lead)

        # Create Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main sheet
            df_main = pd.DataFrame(flattened_leads)
            df_main.to_excel(writer, sheet_name='Leads', index=False)

            # Adjust column widths
            worksheet = writer.sheets['Leads']
            for idx, col in enumerate(df_main.columns):
                max_length = max(
                    df_main[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

        print(f"\n✅ Exported {len(leads)} leads to: {output_path}")

        return output_path

    def export_summary(self, leads: List[Dict]) -> Dict:
        """
        Generate a summary of collected leads.

        Args:
            leads: List of lead dictionaries

        Returns:
            Summary statistics
        """
        summary = {
            'total_leads': len(leads),
            'leads_with_emails': sum(1 for l in leads if l.get('emails')),
            'leads_with_linkedin': sum(1 for l in leads if l.get('linkedin_url') or l.get('url')),
            'unique_companies': len(set(l.get('company', l.get('current_company', '')) for l in leads if l.get('company') or l.get('current_company'))),
            'total_emails': sum(len(l.get('emails', [])) for l in leads)
        }

        return summary
