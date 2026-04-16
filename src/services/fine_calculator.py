class FineCalculator:
    """Calculates fines for overdue books using table-driven rates."""
    
    def __init__(self):
        # Rate tiers: (min_days, max_days, rate_per_day)
        self.tiers = [
            (1, 7, 0.50),
            (8, 30, 1.00),
            (31, float('inf'), 2.00)
        ]
        self.max_fine = 100.00

    def calculate_fine(self, days_overdue: int) -> float:
        if days_overdue <= 0:
            return 0.0
            
        for min_days, max_days, rate in self.tiers:
            if min_days <= days_overdue <= max_days:
                fine = days_overdue * rate
                # Return whichever is smaller: the fine or the maximum cap
                return min(fine, self.max_fine)
                
        return 0.0 