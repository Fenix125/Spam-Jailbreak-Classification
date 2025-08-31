# plot_epoch_overlays_fixed.py
import json
from pathlib import Path
import sys
import matplotlib.pyplot as plt

def main(run_dir: Path):
    state_path = run_dir / "trainer_state.json"
    with open(state_path, "r") as f:
        log_history = json.load(f)["log_history"]

    train_data = [rec for rec in log_history if "loss" in rec]
    val_data = [rec for rec in log_history if "eval_loss" in rec]
    
    epochs = [rec["epoch"] for rec in train_data]
    train_losses = [rec["loss"] for rec in train_data]
    val_losses = [rec["eval_loss"] for rec in val_data]
    
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, train_losses, 'b-o', label='Train Loss')
    plt.plot(epochs, val_losses, 'r-s', label='Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(run_dir / 'loss_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(10, 6))
    for metric in ['eval_accuracy', 'eval_f1', 'eval_precision', 'eval_recall']:
        values = [rec[metric] for rec in val_data]
        label = metric.replace('eval_', '').title()
        plt.plot(epochs, values, '-o', label=label)
    
    plt.xlabel('Epoch')
    plt.ylabel('Score')
    plt.title('Validation Metrics')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(run_dir / 'metrics_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    run_dir = Path(sys.argv[1])
    main(run_dir.resolve())