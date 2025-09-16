import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Step 1: Load dataset (assumes file is in the same folder as this script)
df = pd.read_csv("datasetForTrain2.csv")

# Step 2: Split into features and target
X = df.drop(columns=['is_ransomware'])  # Features
y = df['is_ransomware']                # Target label

# Step 3: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("✅ Model trained successfully and saved as 'random_forest_ransomware.pkl'")
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")
print("\n🧮 Confusion Matrix:\n", conf_matrix)
print("\n📋 Classification Report:\n", report)

# Step 7: Save the trained model
joblib.dump(model, "random_forest_ransomware.pkl")
