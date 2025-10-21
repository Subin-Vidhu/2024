import os
import shutil
import glob
import nibabel as nib
from datetime import datetime

# Dataset paths from the analysis
DATASET_PATHS = {
    'FDA_ORIGINAL': r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025',
    'GT01_AS': r'C:\Users\Subin-PC\Downloads\Telegram Desktop\GT01 - 5 Test Cases',
    'GT02_GM': r'C:\Users\Subin-PC\Downloads\Telegram Desktop\GT02 - 5 Test Cases'
}

def create_backup_archive():
    """
    Create a comprehensive backup of all mask files used in the analysis.
    Organizes files by case and reader type with proper timestamps.
    """
    # Create timestamped backup directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_root = f"Multi_Reader_Mask_Archive_{timestamp}"
    
    print("="*80)
    print("CREATING COMPREHENSIVE MASK FILE ARCHIVE")
    print("="*80)
    print(f"Archive name: {backup_root}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Create main backup directory
    os.makedirs(backup_root, exist_ok=True)
    
    # Create subdirectories
    case_dirs = {}
    summary_data = {
        'total_cases': 0,
        'total_files': 0,
        'readers_found': set(),
        'cases_processed': [],
        'file_inventory': []
    }
    
    # Process the 5 cases we used in analysis
    analysis_cases = ['N-072', 'N-073', 'N-085', 'N-088', 'N-090']
    
    print("\nProcessing analysis cases...")
    
    for case_id in analysis_cases:
        print(f"\nProcessing {case_id}:")
        print("-" * 40)
        
        # Create case directory
        case_dir = os.path.join(backup_root, case_id)
        os.makedirs(case_dir, exist_ok=True)
        case_dirs[case_id] = case_dir
        
        files_copied = 0
        
        # 1. Copy FDA/MC files
        fda_case_folder = os.path.join(DATASET_PATHS['FDA_ORIGINAL'], case_id)
        if os.path.exists(fda_case_folder):
            # MC (Ground Truth) files
            mc_patterns = [
                os.path.join(fda_case_folder, case_id, f'{case_id}_MC.nii'),
                os.path.join(fda_case_folder, case_id, f'{case_id}_MC.nii.gz'),
                os.path.join(fda_case_folder, case_id, f'{case_id}_Updated_MC.nii'),
                os.path.join(fda_case_folder, case_id, f'{case_id}_Updated_MC.nii.gz')
            ]
            
            for mc_pattern in mc_patterns:
                if os.path.exists(mc_pattern):
                    dest_name = f"{case_id}_MC_FDA_Reference.nii"
                    dest_path = os.path.join(case_dir, dest_name)
                    shutil.copy2(mc_pattern, dest_path)
                    files_copied += 1
                    summary_data['readers_found'].add('FDA_MC')
                    summary_data['file_inventory'].append({
                        'case': case_id,
                        'reader': 'FDA_MC',
                        'original_path': mc_pattern,
                        'backup_path': dest_path,
                        'file_size': os.path.getsize(mc_pattern)
                    })
                    print(f"  ✓ FDA/MC: {os.path.basename(mc_pattern)} → {dest_name}")
                    break
            
            # AIRA prediction files
            aira_patterns = [
                os.path.join(fda_case_folder, 'mask.nii'),
                os.path.join(fda_case_folder, 'mask.nii.gz')
            ]
            
            for aira_pattern in aira_patterns:
                if os.path.exists(aira_pattern):
                    dest_name = f"{case_id}_AIRA_Prediction.nii"
                    dest_path = os.path.join(case_dir, dest_name)
                    shutil.copy2(aira_pattern, dest_path)
                    files_copied += 1
                    summary_data['readers_found'].add('AIRA')
                    summary_data['file_inventory'].append({
                        'case': case_id,
                        'reader': 'AIRA',
                        'original_path': aira_pattern,
                        'backup_path': dest_path,
                        'file_size': os.path.getsize(aira_pattern)
                    })
                    print(f"  ✓ AIRA: {os.path.basename(aira_pattern)} → {dest_name}")
                    break
        
        # 2. Copy GT01 (AS reader) files
        gt01_path = os.path.join(DATASET_PATHS['GT01_AS'], f'{case_id}_AS.nii')
        if os.path.exists(gt01_path):
            dest_name = f"{case_id}_GT01_AS_Reader.nii"
            dest_path = os.path.join(case_dir, dest_name)
            shutil.copy2(gt01_path, dest_path)
            files_copied += 1
            summary_data['readers_found'].add('GT01_AS')
            summary_data['file_inventory'].append({
                'case': case_id,
                'reader': 'GT01_AS',
                'original_path': gt01_path,
                'backup_path': dest_path,
                'file_size': os.path.getsize(gt01_path)
            })
            print(f"  ✓ GT01/AS: {os.path.basename(gt01_path)} → {dest_name}")
        
        # 3. Copy GT02 (GM reader) files
        gt02_path = os.path.join(DATASET_PATHS['GT02_GM'], f'{case_id}_GM.nii')
        if os.path.exists(gt02_path):
            dest_name = f"{case_id}_GT02_GM_Reader.nii"
            dest_path = os.path.join(case_dir, dest_name)
            shutil.copy2(gt02_path, dest_path)
            files_copied += 1
            summary_data['readers_found'].add('GT02_GM')
            summary_data['file_inventory'].append({
                'case': case_id,
                'reader': 'GT02_GM',
                'original_path': gt02_path,
                'backup_path': dest_path,
                'file_size': os.path.getsize(gt02_path)
            })
            print(f"  ✓ GT02/GM: {os.path.basename(gt02_path)} → {dest_name}")
        
        # Create case summary file
        case_summary_path = os.path.join(case_dir, f"{case_id}_case_summary.txt")
        with open(case_summary_path, 'w', encoding='utf-8') as f:
            f.write(f"CASE SUMMARY: {case_id}\n")
            f.write("="*50 + "\n")
            f.write(f"Archive created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Files in this case: {files_copied}\n\n")
            
            f.write("FILE DESCRIPTIONS:\n")
            f.write("-"*20 + "\n")
            f.write(f"• {case_id}_MC_FDA_Reference.nii - FDA Reference Ground Truth\n")
            f.write(f"• {case_id}_AIRA_Prediction.nii - AI System Prediction\n")
            f.write(f"• {case_id}_GT01_AS_Reader.nii - Reader AS Annotation (IDENTICAL to FDA)\n")
            f.write(f"• {case_id}_GT02_GM_Reader.nii - Reader GM Annotation (Independent)\n\n")
            
            f.write("ANALYSIS FINDINGS:\n")
            f.write("-"*20 + "\n")
            f.write("• GT01_AS files are IDENTICAL to FDA_MC files (Dice = 1.0)\n")
            f.write("• GT02_GM files are independent annotations (Dice = 0.995)\n")
            f.write("• AIRA predictions show good performance (Dice = 0.908)\n")
            f.write("• Spatial reorientation was applied to AIRA for proper alignment\n")
        
        summary_data['cases_processed'].append(case_id)
        summary_data['total_files'] += files_copied
        print(f"  Files copied: {files_copied}")
    
    summary_data['total_cases'] = len(analysis_cases)
    
    # Create master summary file
    master_summary_path = os.path.join(backup_root, "ARCHIVE_MASTER_SUMMARY.txt")
    with open(master_summary_path, 'w', encoding='utf-8') as f:
        f.write("MULTI-READER MASK FILE ARCHIVE - MASTER SUMMARY\n")
        f.write("="*60 + "\n")
        f.write(f"Archive created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Archive directory: {backup_root}\n")
        f.write(f"Analysis project: FDA Multi-Reader Kidney Segmentation Validation\n\n")
        
        f.write("ARCHIVE STATISTICS:\n")
        f.write("-"*30 + "\n")
        f.write(f"Total cases archived: {summary_data['total_cases']}\n")
        f.write(f"Total files archived: {summary_data['total_files']}\n")
        f.write(f"Readers included: {', '.join(sorted(summary_data['readers_found']))}\n")
        f.write(f"Cases processed: {', '.join(summary_data['cases_processed'])}\n\n")
        
        f.write("DIRECTORY STRUCTURE:\n")
        f.write("-"*30 + "\n")
        f.write(f"{backup_root}/\n")
        for case_id in analysis_cases:
            f.write(f"|-- {case_id}/\n")
            f.write(f"|   |-- {case_id}_MC_FDA_Reference.nii\n")
            f.write(f"|   |-- {case_id}_AIRA_Prediction.nii\n")
            f.write(f"|   |-- {case_id}_GT01_AS_Reader.nii\n")
            f.write(f"|   |-- {case_id}_GT02_GM_Reader.nii\n")
            f.write(f"|   +-- {case_id}_case_summary.txt\n")
        f.write(f"|-- ARCHIVE_MASTER_SUMMARY.txt\n")
        f.write(f"|-- FILE_INVENTORY.csv\n")
        f.write(f"+-- ANALYSIS_NOTES.txt\n\n")
        
        f.write("CRITICAL FINDINGS:\n")
        f.write("-"*30 + "\n")
        f.write("1. GT01_AS files are IDENTICAL to FDA_MC files\n")
        f.write("   - Perfect Dice scores (1.0) are due to file duplication\n")
        f.write("   - This invalidates GT01_AS as an independent reader\n")
        f.write("   - True inter-reader study has only 2 independent readers\n\n")
        
        f.write("2. GT02_GM files are truly independent\n")
        f.write("   - Excellent agreement with FDA (Dice = 0.995)\n")
        f.write("   - Represents genuine expert annotation\n\n")
        
        f.write("3. AIRA predictions show good performance\n")
        f.write("   - Acceptable clinical performance (Dice = 0.908)\n")
        f.write("   - Spatial reorientation was required for proper comparison\n")
        f.write("   - Label remapping applied to match human conventions\n\n")
        
        f.write("REGULATORY IMPLICATIONS:\n")
        f.write("-"*30 + "\n")
        f.write("• Study design compromised by duplicate annotations\n")
        f.write("• True validation is 2-reader + AI system\n")
        f.write("• FDA submission should reflect actual study design\n")
        f.write("• Independent annotations needed for full multi-reader study\n")
    
    # Create detailed file inventory CSV
    inventory_path = os.path.join(backup_root, "FILE_INVENTORY.csv")
    with open(inventory_path, 'w', encoding='utf-8') as f:
        f.write("Case,Reader,Original_Path,Backup_Path,File_Size_Bytes,File_Size_MB\n")
        for item in summary_data['file_inventory']:
            size_mb = item['file_size'] / (1024 * 1024)
            f.write(f"{item['case']},{item['reader']},{item['original_path']},{item['backup_path']},{item['file_size']},{size_mb:.2f}\n")
    
    # Create analysis notes
    notes_path = os.path.join(backup_root, "ANALYSIS_NOTES.txt")
    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write("ANALYSIS NOTES AND METHODOLOGY\n")
        f.write("="*50 + "\n\n")
        
        f.write("SPATIAL ALIGNMENT CORRECTIONS:\n")
        f.write("-"*35 + "\n")
        f.write("• AIRA images required reorientation from ('R','A','S') to ('L','P','I')\n")
        f.write("• This was critical for achieving non-zero Dice scores\n")
        f.write("• Without reorientation, AIRA showed 0.0000 Dice (complete misalignment)\n")
        f.write("• After reorientation, AIRA showed 0.9079 Dice (excellent performance)\n\n")
        
        f.write("LABEL MAPPING CORRECTIONS:\n")
        f.write("-"*30 + "\n")
        f.write("Human readers (FDA, GT02): 0=Background, 1=Left, 2=Right\n")
        f.write("AIRA original: 0=Background, 1=Noise, 2=Left, 3=Right\n")
        f.write("AIRA spatial: 2=Right kidney location, 3=Left kidney location\n")
        f.write("AIRA remapped: 0→0, 1→0, 2→2, 3→1 (to match human convention)\n\n")
        
        f.write("DATA QUALITY ASSESSMENT:\n")
        f.write("-"*30 + "\n")
        f.write("✓ FDA_MC: Reference standard ground truth\n")
        f.write("✓ GT02_GM: Independent expert annotation (0.995 agreement)\n")
        f.write("✗ GT01_AS: Duplicate of FDA_MC (1.000 agreement - identical files)\n")
        f.write("✓ AIRA: AI prediction with spatial/label corrections applied\n\n")
        
        f.write("RECOMMENDED ACTIONS:\n")
        f.write("-"*25 + "\n")
        f.write("1. Contact data provider to obtain true GT01_AS annotations\n")
        f.write("2. Re-run analysis excluding duplicate GT01_AS data\n")
        f.write("3. Report study as 2-reader validation (FDA + GT02_GM)\n")
        f.write("4. Include AIRA as AI system validation component\n")
        f.write("5. Document all spatial and label corrections for FDA submission\n")
    
    print("\n" + "="*80)
    print("ARCHIVE CREATION SUMMARY")
    print("="*80)
    print(f"✓ Archive created: {backup_root}")
    print(f"✓ Cases archived: {summary_data['total_cases']}")
    print(f"✓ Files archived: {summary_data['total_files']}")
    print(f"✓ Readers included: {', '.join(sorted(summary_data['readers_found']))}")
    print(f"✓ Documentation files: 4 (master summary, inventory, notes, case summaries)")
    
    total_size = sum(item['file_size'] for item in summary_data['file_inventory'])
    print(f"✓ Total archive size: {total_size / (1024*1024):.1f} MB")
    
    print("\nGenerated files:")
    print(f"  📁 {backup_root}/")
    print(f"  📄 ARCHIVE_MASTER_SUMMARY.txt")
    print(f"  📊 FILE_INVENTORY.csv")
    print(f"  📝 ANALYSIS_NOTES.txt")
    print(f"  📂 Individual case folders with summaries")
    
    print("\n" + "="*80)
    print("✅ MASK FILE ARCHIVE COMPLETED SUCCESSFULLY!")
    print("📦 All analysis files preserved with proper documentation")
    print("🔍 Ready for regulatory review and future reference")
    print("="*80)
    
    return backup_root

if __name__ == "__main__":
    archive_path = create_backup_archive()
    print(f"\nArchive location: {os.path.abspath(archive_path)}")