import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class EVTripPlanner:
    # Standard battery capacity in kWh (can be modified based on vehicle model)
    TOTAL_BATTERY_CAPACITY = 100  # Example: 100 kWh total capacity

    def __init__(self, source: str, destination: str, time: float, temperature: float, battery_percentage: float):
        """
        Initialize EV Trip Planner with basic trip parameters
        Args:
            source (str): Starting location
            destination (str): End location
            time (float): Expected trip duration in hours
            temperature (float): Ambient temperature in Celsius
            battery_percentage (float): Current battery level (0-100%)
        """
        self.source = source
        self.destination = destination
        self.time = time
        self.temperature = temperature
        self.battery_percentage = min(max(battery_percentage, 0), 100)  # Ensure percentage is between 0 and 100
        self.battery_kwh = (self.battery_percentage / 100) * self.TOTAL_BATTERY_CAPACITY

    def calculate_range_impact(self) -> float:
        """Calculate temperature impact on battery range"""
        # Simplified temperature impact calculation
        # Assumes optimal temperature is 20°C, with reduced efficiency at higher/lower temps
        temp_difference = abs(self.temperature - 20)
        # Rough estimate: 1% reduction per 5°C difference from optimal
        efficiency_loss = (temp_difference / 5) * 0.01
        return 1 - efficiency_loss

    def estimate_energy_needed(self, distance_km: float) -> float:
        """
        Estimate energy needed for the trip
        Args:
            distance_km (float): Trip distance in kilometers
        Returns:
            float: Estimated energy needed in kWh
        """
        # Assume average consumption of 0.2 kWh per km
        base_energy = distance_km * 0.2
        # Apply temperature impact
        temp_efficiency = self.calculate_range_impact()
        return base_energy / temp_efficiency

        # ... (existing code)

    def check_feasibility(self, distance_km: float) -> dict:
        """
        Check if trip is feasible with current battery
        Args:
            distance_km (float): Trip distance in kilometers
        Returns:
            dict: Feasibility assessment and details
        """
        energy_needed = self.estimate_energy_needed(distance_km)
        is_feasible = energy_needed <= self.battery_kwh

        # Calculate battery percentage needed for the trip
        battery_percentage_needed = (energy_needed / self.TOTAL_BATTERY_CAPACITY) * 100

        # Calculate remaining battery percentage after trip
        remaining_percentage = max(0, self.battery_percentage - battery_percentage_needed)

        # Determine feasibility and provide detailed feedback
        if is_feasible:
            feedback = "You have enough battery to do this trip."
        else:
            if energy_needed > self.battery_kwh:
                feedback = f"The trip is not feasible with the current battery level. You need {battery_percentage_needed}% of battery, but you only have {self.battery_percentage}% available. Consider charging your vehicle or fuel up along the way."
            else:
                feedback = f"The trip is not feasible due to the impact of the ambient temperature ({self.temperature}°C). The estimated range is reduced to {trip_plan['estimated_range_km']} km, which is not enough for the {distance_km} km trip. Consider waiting for more favorable weather conditions or charging your vehicle to a higher level."

        return {
            "feasible": is_feasible,
            "feedback": feedback,  # Add feedback to the dictionary
            "energy_needed": round(energy_needed, 2),
            "battery_percentage": round(self.battery_percentage, 1),
            "battery_percentage_needed": round(battery_percentage_needed, 1),
            "remaining_percentage": round(remaining_percentage, 1),
            "temperature_efficiency": round(self.calculate_range_impact() * 100, 1),
            "estimated_range_km": round((self.battery_kwh / 0.2) * self.calculate_range_impact(), 1)
        }
        # ... (existing code)

        # Determine feasibility and provide detailed feedback
        if is_feasible:
            feedback = "You have enough battery to do this trip."
        else:
            if energy_needed > self.battery_kwh:
                feedback = f"The trip is not feasible with the current battery level. You need {battery_percentage_needed}% of battery, but you only have {self.battery_percentage}% available. Consider charging your vehicle or fuel up along the way."
            else:
                feedback = f"The trip is not feasible due to the impact of the ambient temperature ({self.temperature}°C). The estimated range is reduced to {trip_plan['estimated_range_km']} km, which is not enough for the {distance_km} km trip. Consider waiting for more favorable weather conditions or charging your vehicle to a higher level."

        return {
            "feasible": is_feasible,
            "feedback": feedback,
            "energy_needed": round(energy_needed, 2),
            "battery_percentage": round(self.battery_percentage, 1),
            "battery_percentage_needed": round(battery_percentage_needed, 1),
            "remaining_percentage": round(remaining_percentage, 1),
            "temperature_efficiency": round(self.calculate_range_impact() * 100, 1),
            "estimated_range_km": round((self.battery_kwh / 0.2) * self.calculate_range_impact(), 1)
        }

class EVTripPlannerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EV Trip Planner")
        self.geometry("700x600")

        # Initialize variables
        self.source = tk.StringVar()
        self.destination = tk.StringVar()
        self.time = tk.DoubleVar()
        self.temperature = tk.DoubleVar()
        self.battery_percentage = tk.DoubleVar()
        self.distance = tk.DoubleVar()

        # Set default values
        self.temperature.set(20)  # Default temperature 20°C
        self.battery_percentage.set(100)  # Default battery 100%

        self.create_ui()

    def create_ui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('TButton', padding=5)

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Trip Details", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Grid layout for input fields
        ttk.Label(input_frame, text="Starting Location:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.source).grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Destination:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.destination).grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Trip Duration (hours):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.time).grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Ambient Temperature (°C):").grid(row=3, column=0, sticky=tk.W)
        temp_scale = ttk.Scale(input_frame, from_=-20, to=50, orient=tk.HORIZONTAL, variable=self.temperature)
        temp_scale.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Current Battery Level (%):").grid(row=4, column=0, sticky=tk.W)
        battery_scale = ttk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.battery_percentage)
        battery_scale.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Trip Distance (km):").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.distance).grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)

        # Configure grid columns
        input_frame.columnconfigure(1, weight=1)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Plan Trip button
        plan_button = ttk.Button(button_frame, text="Plan Trip", command=self.plan_trip)
        plan_button.pack(pady=10)

        # Result frame
        self.result_frame = ttk.LabelFrame(main_frame, text="Trip Assessment", padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Result labels
        self.result_text = tk.Text(self.result_frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.configure(state='disabled')

    def validate_inputs(self) -> bool:
        """Validate all input fields"""
        if not self.source.get().strip():
            messagebox.showerror("Error", "Please enter a starting location")
            return False
        if not self.destination.get().strip():
            messagebox.showerror("Error", "Please enter a destination")
            return False
        try:
            if self.time.get() <= 0:
                messagebox.showerror("Error", "Trip duration must be greater than 0")
                return False
            if self.distance.get() <= 0:
                messagebox.showerror("Error", "Distance must be greater than 0")
                return False
        except tk.TclError:
            messagebox.showerror("Error", "Please enter valid numbers for duration and distance")
            return False
        return True
    # ... (existing code)

    def plan_trip(self):
        if not self.validate_inputs():
            return

        planner = EVTripPlanner(
            self.source.get(),
            self.destination.get(),
            self.time.get(),
            self.temperature.get(),
            self.battery_percentage.get()
        )

        trip_plan = planner.check_feasibility(self.distance.get())

        # Format the result text
        result_text = f"""Trip Assessment:

🚗 Route: {self.source.get()} to {self.destination.get()}
📏 Distance: {self.distance.get()} km
⏱️ Expected Duration: {self.time.get()} hours
🌡️ Temperature: {self.temperature.get()}°C

Battery Status:
📊 Current Battery Level: {trip_plan['battery_percentage']}%
🔋 Battery Needed for Trip: {trip_plan['battery_percentage_needed']}%
⚡ Remaining Battery: {trip_plan['remaining_percentage']}%

Performance Metrics:
🌡️ Temperature Efficiency: {trip_plan['temperature_efficiency']}%
📍 Estimated Range: {trip_plan['estimated_range_km']} km

Status: {'✅ Your Trip is On!!Hurray!' if trip_plan['feasible'] else '❌ You need to ensure below actions to make this trip'}
{trip_plan['feedback']}
"""

        # Update result text
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
        self.result_text.configure(state='disabled')
if __name__ == "__main__":
  app = EVTripPlannerUI()
  app.mainloop()