TELEMETRY_FOR_DEVICE = """
    SELECT *
    FROM telemetry_record
    WHERE device_serial_number = {device_serial_number:String} AND timestamp > {timestamp:DateTime}
    ORDER BY timestamp DESC
"""
