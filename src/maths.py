def clamp(value: int | float, minimum: int | float, maximum: int | float):
	return max(minimum, min(value, maximum))
