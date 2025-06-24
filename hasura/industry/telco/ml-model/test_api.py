#!/usr/bin/env python3
"""
Test script for the Telecom Churn Prediction API
"""

import requests
import json
import time

# API endpoint
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.json()}")
    return response.status_code == 200

def test_prediction():
    """Test churn prediction with sample data"""
    print("\nTesting churn prediction...")
    
    # Sample customer data - high risk customer (based on real data patterns)
    high_risk_customer = {
        "customerId": 12345,
        "satisfactionScore": 2,    # Low satisfaction (real data: churned avg 5.3)
        "segment": "Student",      # Highest churn segment (71.4%)
        "dataAllocationGb": 10,
        "dataUsedGb": 15.5,       # Data overage
        "totalAmount": 25.50,
        "paymentStatus": "Overdue", # 81.2% churn rate for overdue
        "downloadSpeed": 12.2,     # Poor network performance
        "uploadSpeed": 3.1,
        "latency": 150,           # High latency (churned avg: 111ms)
        "serviceInteractionCount": 6, # Frequent interactions
        "avgResolutionTime": 36.0,
        "feedbackRating": 0.5,    # Very low feedback
        "callDurationMinutes": 45.8
    }
    
    # Sample customer data - low risk customer (based on real data patterns)
    low_risk_customer = {
        "customerId": 67890,
        "satisfactionScore": 8,    # High satisfaction (retained avg: 6.1)
        "segment": "Premium",      # Lowest churn segment (43.1%)
        "dataAllocationGb": 50,
        "dataUsedGb": 35.2,       # Under allocation
        "totalAmount": 180.00,
        "paymentStatus": "Paid",   # 49.3% churn rate for paid
        "downloadSpeed": 85.5,     # Good network performance
        "uploadSpeed": 25.3,
        "latency": 35,            # Low latency (retained avg: 100ms)
        "serviceInteractionCount": 1, # Few interactions
        "avgResolutionTime": 2.0,
        "feedbackRating": 4.8,    # High feedback
        "callDurationMinutes": 5.2
    }
    
    # Test high risk customer
    print("\n--- High Risk Customer ---")
    response = requests.post(f"{BASE_URL}/predict", json=high_risk_customer)
    if response.status_code == 200:
        result = response.json()
        print(f"Customer ID: {result['customerId']}")
        print(f"Churn Probability: {result['churnProbability']:.1%}")
        print(f"Risk Level: {result['churnRisk']}")
        print(f"Risk Factors: {', '.join(result['riskFactors'])}")
        print(f"Recommendations: {', '.join(result['recommendations'])}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test low risk customer
    print("\n--- Low Risk Customer ---")
    response = requests.post(f"{BASE_URL}/predict", json=low_risk_customer)
    if response.status_code == 200:
        result = response.json()
        print(f"Customer ID: {result['customerId']}")
        print(f"Churn Probability: {result['churnProbability']:.1%}")
        print(f"Risk Level: {result['churnRisk']}")
        print(f"Risk Factors: {', '.join(result['riskFactors'])}")
        print(f"Recommendations: {', '.join(result['recommendations'])}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_model_info():
    """Test model info endpoint"""
    print("\n--- Model Information ---")
    response = requests.get(f"{BASE_URL}/model/info")
    if response.status_code == 200:
        info = response.json()
        print(f"Model Type: {info['model_type']}")
        print(f"Status: {info['status']}")
        print(f"Features: {len(info['features'])} features")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_retrain():
    """Test model retraining"""
    print("\n--- Testing Model Retraining ---")
    response = requests.post(f"{BASE_URL}/retrain")
    if response.status_code == 200:
        result = response.json()
        print(f"Retraining Status: {result['status']}")
        print(f"Model Accuracy: {result['accuracy']:.1%}")
        print(f"Trained At: {result['trained_at']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("TELECOM CHURN PREDICTION API TESTS")
    print("=" * 50)
    
    # Wait for service to be ready
    print("Waiting for service to be ready...")
    max_retries = 30
    for i in range(max_retries):
        try:
            if test_health():
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            if i == max_retries - 1:
                print("Service not available after 30 seconds")
                return
    
    # Run tests
    test_prediction()
    test_model_info()
    test_retrain()
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()