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
            cnh = fake.bothify(text='######')
        cnhs.add(cnh)
        nome = fake.name()
        cnh_valid = random.randint(0, 1)
        placa = random.choice(taxi_placas)
        file.write(f"INSERT INTO Motorista (CNH, Nome, CNHValid, Placa) VALUES ('{cnh}', '{nome}', {cnh_valid}, '{placa}');\n")


def generate_zona_data(n, file):
    zonas = set()
    while len(zonas) < n:
        zona = fake.unique.city()
        zonas.add(zona)
    for zona in zonas:
        file.write(f"INSERT INTO Zona (Zona) VALUES ('{zona}');\n")


def main():
    num_taxi = 10_000  
    num_cliente = 10_000  
    num_corrida = 10_000  
    num_motorista = 10_000  
    num_zona = 10_000  

    with open('generated_data.sql', 'w', encoding='utf-8') as f:
        taxi_placas = generate_taxi_data(num_taxi, f)
        cliente_ids = generate_cliente_data(num_cliente, f)
        generate_corrida_data(num_corrida, cliente_ids, taxi_placas, f)
        generate_motorista_data(num_motorista, taxi_placas, f)
        generate_zona_data(num_zona, f)

if __name__ == "__main__":
    main()