import json
import matplotlib.pyplot as plt

# Load updated data
with open("charts/predictions_data.json", "r") as json_file:
    data = json.load(json_file)

# Extract data
resolutions = data["res"]
predictions_per_second = data["preds/s"]

# Plot the bar chart
plt.figure(figsize=(8, 6))
plt.bar(resolutions, predictions_per_second, color="skyblue")

# Add labels and title
plt.xlabel("Resolution")
plt.ylabel("Predictions per Second")
plt.title("Predicciones por segundo para diferentes resoluciones")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
# plt.show()

plt.savefig("charts/predictions_plot.png")  # You can change the file format (e.g., .jpg, .pdf)

# Close the plot to avoid display (optional)
plt.close()

print("Plot saved to predictions_plot.png")