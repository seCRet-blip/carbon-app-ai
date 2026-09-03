"""
Main entry point for carbon credit eligibility classification training
"""

import argparse
from training import train_advanced_model


def diagnose_dataset():
    """Analyze dataset for training issues"""
    import pandas as pd
    from collections import Counter
    
    print("🔍 DATASET DIAGNOSIS")
    print("="*50)
    
    # Load all datasets
    try:
        train_df = pd.read_csv('carbon_dataset/train.csv')
        val_df = pd.read_csv('carbon_dataset/val.csv')
        test_df = pd.read_csv('carbon_dataset/test.csv')
        
        print("ORIGINAL OTAGO DATASETS:")
        for name, df in [("Train", train_df), ("Val", val_df), ("Test", test_df)]:
            eligible = len(df[df['label'] == 'eligible'])
            ineligible = len(df[df['label'] == 'ineligible'])
            ratio = eligible / ineligible if ineligible > 0 else 0
            
            print(f"\n{name} Set:")
            print(f"  Eligible: {eligible:,}")
            print(f"  Ineligible: {ineligible:,}")
            print(f"  Ratio: 1:{ineligible/eligible:.1f}")
            
            if ratio < 0.1:
                print(f"  ⚠️  SEVERE IMBALANCE - Consider oversampling eligible class")
                
    except FileNotFoundError as e:
        print(f"❌ Error loading original dataset files: {e}")
        print("Make sure the CSV files exist in the carbon_dataset/ directory")
    
    # Check for multi-region datasets
    try:
        multi_train = pd.read_csv('carbon_dataset/multi_region_train.csv')
        multi_val = pd.read_csv('carbon_dataset/multi_region_val.csv')
        multi_test = pd.read_csv('carbon_dataset/multi_region_test.csv')
        
        print(f"\n{'='*50}")
        print("MULTI-REGION DATASETS AVAILABLE:")
        
        for name, df in [("Multi Train", multi_train), ("Multi Val", multi_val), ("Multi Test", multi_test)]:
            eligible = len(df[df['label'] == 'eligible'])
            ineligible = len(df[df['label'] == 'ineligible'])
            otago_count = len(df[df['region'] == 'otago']) if 'region' in df.columns else 0
            christchurch_count = len(df[df['region'] == 'christchurch']) if 'region' in df.columns else 0
            
            print(f"\n{name} Set:")
            print(f"  Total: {len(df):,}")
            print(f"  Eligible: {eligible}, Ineligible: {ineligible}")
            print(f"  Otago: {otago_count:,}, Christchurch: {christchurch_count:,}")
            
        print("\n✅ Multi-region datasets ready! Use --multi-region flag")
                
    except FileNotFoundError:
        print(f"\n{'='*50}")
        print("Multi-region datasets not found.")
        print("Run: py create_multi_region_dataset.py")


def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description='Train Carbon Credit Eligibility Classifier')
    parser.add_argument('--model', type=str, default='efficientnet', 
                       choices=['efficientnet', 'resnet', 'both'],
                       help='Model type to use')
    parser.add_argument('--mixup', action='store_true', default=False,
                       help='Use mixup augmentation')
    parser.add_argument('--ensemble', action='store_true', default=False,
                       help='Use ensemble of models')
    parser.add_argument('--diagnose', action='store_true', default=False,
                       help='Run dataset diagnosis only')
    parser.add_argument('--multi-region', action='store_true', default=False,
                       help='Use multi-region training (Otago + Christchurch)')
    
    args = parser.parse_args()
    
    if args.diagnose:
        diagnose_dataset()
        return
    
    print("🚀 CARBON CREDIT ELIGIBILITY CLASSIFIER")
    print("="*60)
    
    if args.multi_region:
        print("🌍 MULTI-REGION MODE: Will train on all NZ regions (see multi_region_train.csv)")
    else:
        print("🏔️ SINGLE REGION MODE: Will train on Otago data only (see train.csv)")
        
    print("Dependencies: pip install albumentations torch torchvision tqdm scikit-learn")
    print()
    
    # Run dataset diagnosis first
    diagnose_dataset()
    print("\n" + "="*60)
    
    # Train model with specified configuration
    model = train_advanced_model(
        model_type=args.model,
        use_mixup=args.mixup,
        use_ensemble=args.ensemble,
        multi_region=args.multi_region
    )
    
    if args.multi_region:
        print("\n🌍 Multi-region training completed! Model trained on all NZ regions.")
    else:
        print("\n🎉 Training completed! Model trained on Otago only.")


if __name__ == "__main__":
    main()
