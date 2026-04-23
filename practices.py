class SistemaLogs:
    def __init__(self):
        self.logs = []

    def agregar_log(self, log):
        # PSEUDOCODIGO:
        # agregar log a la lista de logs
        self.logs.append(log)
        pass

    def filtrar_por_severidad(self, severidad):
        resultado = []
        for log in self.logs:
            if log["severity"] == severidad:
                resultado.append(log)
        return resultado
    
        # PSEUDOCODIGO:
        # crear lista resultado vacía
        # para cada log en self.logs:
        #   si la severidad del log es igual a severidad:
        #     agregar log a resultado
        # retornar resultado


sistema = SistemaLogs()

sistema.agregar_log({"timestamp": "2026-02-21", "servicio": "auth-service", "severity": "INFO", "hora": "10:30:00", "mensaje": "Servidor iniciado"})
sistema.agregar_log({"timestamp": "2026-02-21", "servicio": "db-service", "severity": "ERROR", "hora": "10:45:12", "mensaje": "Conexión a base de datos fallida"})
sistema.agregar_log({"timestamp": "2026-02-21", "servicio": "api-gateway", "severity": "WARNING", "hora": "11:00:05", "mensaje": "Timeout en request externo"})

logs_error = sistema.filtrar_por_severidad("ERROR")
for log in logs_error:
    print(log)
