import json
from core import orchestrator

# -------------------------------
# LOAD GROUND TRUTH
# -------------------------------
with open("data/ground_truth.json", "r") as f:
    ground_truth = {
        item["project_id"]: item["expected_risk"]
        for item in json.load(f)
    }

# -------------------------------
# RUN MODEL
# -------------------------------
orchestrator = orchestrator.RiskOrchestrator()
results = orchestrator.run()

# -------------------------------
# METRICS INIT
# -------------------------------
total = len(results)
correct = 0

# confusion matrix
labels = ["LOW", "MEDIUM", "HIGH"]
confusion = {l: {k: 0 for k in labels} for l in labels}

print("\n===== EVALUATION =====\n")

# -------------------------------
# EVALUATION LOOP
# -------------------------------
for r in results:
    pid = r["project_id"]

    predicted = r["final_risk"].get("risk_level", "UNKNOWN")
    expected = ground_truth.get(pid, "UNKNOWN")

    if predicted == expected:
        correct += 1

    # update confusion matrix
    if expected in labels and predicted in labels:
        confusion[expected][predicted] += 1

    print(f"Project {pid}")
    print(f"Predicted: {predicted}")
    print(f"Expected:  {expected}")
    print(f"Match: {'✅' if predicted == expected else '❌'}\n")

# -------------------------------
# ACCURACY
# -------------------------------
accuracy = correct / total if total > 0 else 0
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")

# -------------------------------
# CONFUSION MATRIX
# -------------------------------
print("\n📊 Confusion Matrix:\n")

print(f"{'':10} LOW   MED   HIGH")
for actual in labels:
    row = confusion[actual]
    print(f"{actual:10} {row['LOW']:5} {row['MEDIUM']:5} {row['HIGH']:5}")