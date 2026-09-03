"""
Count Carbon Credit Eligible Data Points
Analyzes the labels.csv file to show distribution of eligible/ineligible/uncertain labels
"""

import pandas as pd
from pathlib import Path

def count_labels():
    """Count and analyze labels from the CSV file"""
    
    # Path to your labels file
    labels_path = Path('./carbon_dataset/labels.csv')
    
    if not labels_path.exists():
        print(f"❌ Labels file not found at: {labels_path}")
        print("Run createData.py first to generate labels.")
        return
    
    # Load the data
    print("📊 Loading labels data...")
    df = pd.read_csv(labels_path)
    
    print(f"✓ Loaded {len(df)} total data points\n")
    
    # Count by label type
    print("="*50)
    print("CARBON CREDIT ELIGIBILITY BREAKDOWN")
    print("="*50)
    
    label_counts = df['label'].value_counts()
    total = len(df)
    
    for label, count in label_counts.items():
        percentage = (count / total) * 100
        status_emoji = "✅" if label == "eligible" else "❌" if label == "ineligible" else "❓"
        print(f"{status_emoji} {label.upper():<12}: {count:>6,} ({percentage:5.1f}%)")
    
    print("-" * 50)
    print(f"📈 TOTAL IMAGES    : {total:>6,} (100.0%)")
    
    # Confidence analysis
    if 'confidence' in df.columns:
        print("\n" + "="*50)
        print("CONFIDENCE ANALYSIS")
        print("="*50)
        
        high_conf = df[df['confidence'] > 0.7]
        med_conf = df[(df['confidence'] >= 0.5) & (df['confidence'] <= 0.7)]
        low_conf = df[df['confidence'] < 0.5]
        
        print(f"🔥 High Confidence (>70%): {len(high_conf):>6,} ({len(high_conf)/total*100:5.1f}%)")
        print(f"⚡ Med Confidence (50-70%): {len(med_conf):>6,} ({len(med_conf)/total*100:5.1f}%)")
        print(f"⚠️  Low Confidence (<50%): {len(low_conf):>6,} ({len(low_conf)/total*100:5.1f}%)")
        
        # High confidence eligible count
        high_conf_eligible = df[(df['confidence'] > 0.7) & (df['label'] == 'eligible')]
        print(f"\n🎯 High-Confidence ELIGIBLE: {len(high_conf_eligible):>6,} images")
    
    # Training data suitability
    print("\n" + "="*50)
    print("TRAINING DATA SUITABILITY")
    print("="*50)
    
    # Remove uncertain labels for training
    training_ready = df[df['label'] != 'uncertain']
    eligible_for_training = training_ready[training_ready['label'] == 'eligible']
    ineligible_for_training = training_ready[training_ready['label'] == 'ineligible']
    
    print(f"🤖 Training Ready Total: {len(training_ready):>6,}")
    print(f"   ├─ Eligible        : {len(eligible_for_training):>6,}")
    print(f"   └─ Ineligible      : {len(ineligible_for_training):>6,}")
    
    # Check balance
    if len(eligible_for_training) > 0 and len(ineligible_for_training) > 0:
        ratio = len(eligible_for_training) / len(ineligible_for_training)
        if 0.5 <= ratio <= 2.0:
            print(f"✅ Good class balance (ratio: {ratio:.2f})")
        else:
            print(f"⚠️  Imbalanced classes (ratio: {ratio:.2f})")
    elif len(eligible_for_training) == 0:
        print("❌ NO ELIGIBLE IMAGES - Cannot train model")
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"✅ Ready for CNN training: {len(training_ready):,} images")
    print(f"🎯 Carbon credit eligible: {len(df[df['label'] == 'eligible']):,} images")
    
    return df

if __name__ == "__main__":
    count_labels()
