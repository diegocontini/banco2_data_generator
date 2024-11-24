from faker import Faker
import random

fake = Faker()


def generate_taxi_data(n, file):
    taxi_placas = set()
    while len(taxi_placas) < n:
        placa = fake.license_plate()[:7]
        if placa not in taxi_placas:
            marca = fake.company()
            modelo = fake.word()
            ano_fab = fake.year()
            licenca = fake.license_plate()[:9]
            taxi_placas.add(placa)
            file.write(f"INSERT INTO Taxi (Placa, Marca, Modelo, AnoFab, Licenca) VALUES ('{placa}', '{marca}', '{modelo}', '{ano_fab}', '{licenca}');\n")
    return list(taxi_placas)


def generate_cliente_data(n, file):
    cliente_ids = []
    for i in range(1, n + 1):
        cpf = fake.unique.bothify(text='###.###.###-##')
        nome = fake.name()
        file.write(f"INSERT INTO Cliente (CliId, CPF, Nome) VALUES ({i}, '{cpf}', '{nome}');\n")
        cliente_ids.append(i)
    return cliente_ids


def generate_corrida_data(n, cliente_ids, taxi_placas, file):
    for _ in range(n):
        cli_id = random.choice(cliente_ids)
        placa = random.choice(taxi_placas)
        data_pedido = fake.date_this_decade()
        file.write(f"INSERT INTO Corrida (CliId, Placa, DataPedido) VALUES ({cli_id}, '{placa}', '{data_pedido}');\n")


def generate_motorista_data(n, taxi_placas, file):
    cnhs = set()
    for _ in range(n):
        cnh = fake.bothify(text='######')
        while cnh in cnhs:
            cnh = fake.bothify(text='######');
        nome = fake.name()
        cnh_valid = random.randint(0, 1)
        placa = random.choice(taxi_placas)
        file.write(f"INSERT INTO Motorista (CNH, Nome, CNHValid, Placa) VALUES ('{cnh}', '{nome}', {cnh_valid}, '{placa}');\n")
        cnhs.add(cnh)
    return cnhs


def generate_zona_data(n, file):
    zonas = set()
    while len(zonas) < n:
        zona = fake.unique.city()
        zonas.add(zona)
    for zona in zonas:
        file.write(f"INSERT INTO Zona (Zona) VALUES ('{zona}');\n")

def generate_zona_data(n, file):
    zonas = set()
    while len(zonas) < n:
        zona = fake.unique.city()
        zonas.add(zona)
    for zona in zonas:
        file.write(f"INSERT INTO Zona (Zona) VALUES ('{zona}');\n")
    return list(zonas)

def generate_fila_data(n, zonas, cnhs, file):
    cnhs_list = list(cnhs)  # Convert set to list
    for _ in range(n):
        zona = random.choice(zonas)
        cnh = random.choice(cnhs_list)
        data_hora_in = fake.date_time()
        data_hora_out = fake.date_time_between(start_date=data_hora_in)
        km_in = fake.random_int(min=0, max=100000)
        file.write(f"INSERT INTO Fila (Zona, CNH, DataHoraIn, DataHoraOut, KmIn) VALUES ('{zona}', '{cnh}', '{data_hora_in}', '{data_hora_out}', {km_in}) ON CONFLICT DO NOTHING;\n")

def generate_cliente_empresa_data(n, cliente_ids, file):
    for _ in range(n):
        cli_id = random.choice(cliente_ids)
        nome = fake.company()
        cnpj = fake.unique.bothify(text='##############')
        file.write(f"INSERT INTO ClienteEmpresa (CliId, Nome, CNPJ) VALUES ({cli_id}, '{nome}', '{cnpj}') ON CONFLICT DO NOTHING;\n")

def main():
    num_taxi = 10_000  
    num_cliente = 10_000  
    num_corrida = 100_000  
    num_motorista = 10_000  
    num_zona = 10_000  
    num_fila = 10_000  
    num_cliente_empresa = 10_000  

    with open('generated_data.sql', 'w', encoding='utf-8') as f:
        taxi_placas = generate_taxi_data(num_taxi, f)
        cliente_ids = generate_cliente_data(num_cliente, f)
        generate_corrida_data(num_corrida, cliente_ids, taxi_placas, f)
        cnhs = generate_motorista_data(num_motorista, taxi_placas, f)
        zonas = generate_zona_data(num_zona, f)
        generate_fila_data(num_fila, zonas, cnhs, f)
        generate_cliente_empresa_data(num_cliente_empresa, cliente_ids, f)

if __name__ == "__main__":
    main()