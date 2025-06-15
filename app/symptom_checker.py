def check_symptoms(symptoms):
    symptoms = symptoms.lower()

    if "fever" in symptoms or "temperature" in symptoms:
        return (
            "You may have a viral infection or flu.",
            [
                {"name": "Paracetamol", "dosage": "500mg, twice daily"},
                {"name": "Dolo 650", "dosage": "650mg, after meals"},
            ]
        )

    elif "cough" in symptoms:
        return (
            "Persistent cough may indicate bronchitis or COVID-19.",
            [
                {"name": "Benadryl", "dosage": "10ml, 3 times daily"},
                {"name": "Honitus", "dosage": "5ml, 4 times daily"}
            ]
        )

    elif "headache" in symptoms:
        return (
            "Headaches could be due to stress or migraines.",
            [
                {"name": "Disprin", "dosage": "1 tablet as needed"},
                {"name": "Saridon", "dosage": "1 tablet, max 2/day"}
            ]
        )

    elif "fatigue" in symptoms or "tired" in symptoms:
        return (
            "Fatigue may be due to low nutrition or anemia.",
            [
                {"name": "Revital H", "dosage": "1 capsule daily"},
                {"name": "Iron supplement", "dosage": "as prescribed"}
            ]
        )

    elif "chest pain" in symptoms:
        return (
            "Chest pain could be serious. Seek urgent medical attention.",
            []
        )

    elif "rash" in symptoms or "skin irritation" in symptoms:
        return (
            "Rash might be allergic or infectious.",
            [
                {"name": "Cetirizine", "dosage": "10mg, once daily"},
                {"name": "Calamine Lotion", "dosage": "Apply twice daily"}
            ]
        )

    elif "sore throat" in symptoms:
        return (
            "Sore throat is often caused by viral infections.",
            [
                {"name": "Strepsils", "dosage": "1 lozenge every 3 hrs"},
                {"name": "Salt Water Gargle", "dosage": "3 times a day"}
            ]
        )

    else:
        return (
            "Sorry, symptom not recognized. Please consult a doctor.",
            []
        )

