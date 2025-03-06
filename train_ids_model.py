from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Import feature extraction
import featureextraction  # This ensures X_train, y_train, X_test, y_test are loaded

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(featureextraction.X_train, featureextraction.y_train)

# Evaluate model
y_pred = clf.predict(featureextraction.X_test)
accuracy = accuracy_score(featureextraction.y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model & vectorizer
joblib.dump(clf, "ml_ids_model.pkl")
joblib.dump(featureextraction.vectorizer, "vectorizer.pkl")

print("✅ Model training complete! Saved as ml_ids_model.pkl")
