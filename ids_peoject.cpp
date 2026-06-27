#include <iostream>
using namespace std;

int main() {

    int mode;
    cout << "=========== Accident Intelligence System ===========\n";
    cout << "1. Predict Risk (Before Accident)\n";
    cout << "2. Accident Impact Analysis (After Accident)\n";
    cout << "Choice: ";
    cin >> mode;

    // =====================================================
    // ?? MODE 1: RISK PREDICTION
    // =====================================================
    if (mode == 1) {

        int vehicleType, category, speed, weather, surface, visibility;
        int driverCond, company, light, roadCond;
        int riskScore = 0;

        cout << "\n--- Vehicle Information ---\n";
        cout << "Vehicle Type:\n1.Car 2.Bike 3.Truck 4.Bus\nChoice: ";
        cin >> vehicleType;

        cout << "Vehicle Category:\n1.Normal 2.Sports\nChoice: ";
        cin >> category;

        cout << "Company Quality:\n1.High-End 2.Mid 3.Low\nChoice: ";
        cin >> company;

        cout << "Enter Speed (km/h): ";
        cin >> speed;

        cout << "\n--- Environment Conditions ---\n";
        cout << "Weather:\n1.Clear 2.Light Rain 3.Heavy Rain 4.Snow/Storm\nChoice: ";
        cin >> weather;

        cout << "Road Surface:\n1.Dry 2.Wet 3.Slippery/Ice\nChoice: ";
        cin >> surface;

        cout << "Visibility:\n1.Clear 2.Fog 3.Very Low (Dust/Smoke/Night)\nChoice: ";
        cin >> visibility;

        // ? NEW: LIGHT
        cout << "Lighting Condition:\n";
        cout << "1.Daylight\n2.Night (Street Lights ON)\n3.Dark (No Lights)\nChoice: ";
        cin >> light;

        // ? NEW: ROAD CONDITION
        cout << "Road Condition:\n";
        cout << "1.Normal\n2.Under Construction\n3.Damaged (Potholes/Bumps)\n4.Obstruction (Debris/Objects)\nChoice: ";
        cin >> roadCond;

        cout << "\n--- Driver Condition ---\n";
        cout << "1.Normal 2.Using Phone 3.Drunk 4.Sleepy\nChoice: ";
        cin >> driverCond;

        // ===== LOGIC =====
        if (speed > 80) riskScore += 3;
        else if (speed > 50) riskScore += 2;

        if (category == 2) riskScore += 2;
        if (vehicleType == 2) riskScore += 2;
        if (vehicleType == 3) riskScore += 1;

        if (weather >= 2) riskScore += 2;
        if (surface >= 2) riskScore += 2;
        if (visibility >= 2) riskScore += 2;

        if (driverCond >= 2) riskScore += 3;

        if (company == 3) riskScore += 2;
        else if (company == 2) riskScore += 1;

        // ? NEW LOGIC
        if (light == 2) riskScore += 1;
        if (light == 3) riskScore += 2;

        if (roadCond == 2) riskScore += 1;
        if (roadCond == 3) riskScore += 2;
        if (roadCond == 4) riskScore += 2;

        // ===== OUTPUT =====
        cout << "\n======= Risk Prediction Result =======\n";

        if (riskScore >= 11)
            cout << "Risk Level: HIGH (Accident Highly Likely)\n";
        else if (riskScore >= 6)
            cout << "Risk Level: MEDIUM (Risk Present)\n";
        else
            cout << "Risk Level: LOW (Relatively Safe)\n";

        cout << "\nKey Risk Factors:\n";

        if (speed > 80) cout << "- High Speed\n";
        if (weather >= 2) cout << "- Bad Weather\n";
        if (surface >= 2) cout << "- Slippery Road\n";
        if (visibility >= 2) cout << "- Poor Visibility\n";
        if (driverCond >= 2) cout << "- Driver Condition Risk\n";

        // ? NEW OUTPUT
        if (light == 3) cout << "- Poor Lighting Conditions\n";
        if (roadCond >= 2) cout << "- Unsafe Road Condition\n";

        cout << "=====================================\n";
    }

    // =====================================================
    // ?? MODE 2: IMPACT ANALYSIS
    // =====================================================
    else if (mode == 2) {

        int vehicleType, category, passengers, speed;
        int light, visibility, weather, surface;
        int driverCond, fault, impactType;
        int airbags = 0, helmet = 0, truckLoad = 0;

        int severityScore = 0;

        cout << "\n--- Accident Basic Info ---\n";
        cout << "Vehicle Type:\n1.Car 2.Bike 3.Truck 4.Bus\nChoice: ";
        cin >> vehicleType;

        cout << "Vehicle Category:\n1.Normal 2.Sports\nChoice: ";
        cin >> category;

        cout << "Passengers Count: ";
        cin >> passengers;

        cout << "Estimated Speed at Impact: ";
        cin >> speed;

        cout << "\n--- Environment ---\n";
        cout << "Lighting:\n1.Daylight 2.Night with Lights 3.Dark (No Lights)\nChoice: ";
        cin >> light;

        cout << "Visibility:\n1.Clear 2.Foggy 3.Low (Dust/Smoke/Rain)\nChoice: ";
        cin >> visibility;

        cout << "Weather:\n1.Clear 2.Rain 3.Storm/Snow\nChoice: ";
        cin >> weather;

        cout << "Road Surface:\n1.Dry 2.Wet 3.Icy/Slippery\nChoice: ";
        cin >> surface;

        cout << "\n--- Driver State ---\n";
        cout << "1.Normal 2.Phone Use 3.Drunk 4.Sleepy\nChoice: ";
        cin >> driverCond;

        cout << "Driver At Fault?\n1.Yes 2.No\nChoice: ";
        cin >> fault;

        cout << "\nImpact Nature:\n1.High-Speed Collision 2.Side/Turning Crash 3.Minor Impact\nChoice: ";
        cin >> impactType;

        if (vehicleType == 1) {
            cout << "Airbags Deployed?\n1.Yes 2.No\nChoice: ";
            cin >> airbags;
        }
        else if (vehicleType == 2) {
            cout << "Helmet Used?\n1.Yes 2.No\nChoice: ";
            cin >> helmet;
        }
        else if (vehicleType == 3) {
            cout << "Truck Load:\n1.Empty 2.Light 3.Heavy 4.Hazardous\nChoice: ";
            cin >> truckLoad;
        }

        // ===== SCORING =====
        if (speed > 70) severityScore += 3;
        if (category == 2) severityScore += 2;
        if (weather >= 2) severityScore += 2;
        if (surface >= 2) severityScore += 2;
        if (visibility >= 2) severityScore += 2;
        if (driverCond >= 2) severityScore += 3;
        if (impactType == 1) severityScore += 3;
        if (impactType == 2) severityScore += 2;

        if (vehicleType == 2 && helmet == 2) severityScore += 3;
        if (vehicleType == 1 && airbags == 1) severityScore -= 1;
        if (vehicleType == 3 && truckLoad >= 3) severityScore += 2;

        // ===== OUTPUT =====
        cout << "\n=========== Accident Intelligence Report ===========\n";

        cout << "\nAccident Scenario:\n";
        if (impactType == 1)
            cout << "A high-speed collision with strong force impact.\n";
        else if (impactType == 2)
            cout << "A side/turning collision, likely at intersection.\n";
        else
            cout << "A low-speed minor collision.\n";

        cout << "\nInjury Analysis:\n";
        if (severityScore >= 10)
            cout << "Driver: SEVERE\nPassengers: HIGH RISK\n";
        else if (severityScore >= 6)
            cout << "Driver: MODERATE\nPassengers: MODERATE\n";
        else
            cout << "Driver: MINOR\nPassengers: LOW\n";

        cout << "\nVehicle Damage:\n";
        if (severityScore >= 10)
            cout << "Severe Structural Damage\n";
        else if (severityScore >= 6)
            cout << "Moderate Damage\n";
        else
            cout << "Minor Damage\n";

        cout << "\nDetailed Reasoning:\n";
        if (driverCond == 2) cout << "- Driver distracted (phone)\n";
        if (driverCond == 3) cout << "- Driver intoxicated\n";
        if (driverCond == 4) cout << "- Driver fatigue\n";
        if (weather >= 2) cout << "- Bad weather\n";
        if (surface >= 2) cout << "- Slippery road\n";
        if (visibility >= 2) cout << "- Poor visibility\n";
        if (light == 3) cout << "- No lighting\n";

        cout << "\n===================================================\n";
    }

    else {
        cout << "Invalid Choice!\n";
    }

    return 0;
}
