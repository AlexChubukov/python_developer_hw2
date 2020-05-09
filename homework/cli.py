import patient
import click
import sqlite3

@click.group()
def cli():
   pass

@cli.command()
def count():
    collection = patient.PatientCollection()
    print(f"Количество пациентов в БД: {len(collection.data)} ")

@cli.command()
@click.argument('limit', default=10)
def show(limit):
    pc = patient.PatientCollection()
    for p in pc.limit(limit):
        print(p)



@cli.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--birth-date',  help='Birth date of Patient', type= str)
@click.option('--phone',  help='Mobile phone of Patient', type= str)
@click.option('--document-type',  help='Document type of Patient', type= str)
@click.option('--document-number', help='Document number of Patient', type=str)
def create(first_name, last_name, birth_date, phone, document_type, document_number):
    p = patient.Patient(first_name, last_name, birth_date, phone, document_type, document_number)
    p.save()
    print(f'Записан пациент: {p}')

if __name__=="__main__":
    conn = sqlite3.connect("Covid.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
       first_name varchar(15),
       last_name varchar(15),
       birth_date char(10),
       phone char(16),
       document_type varchar(19),
       document_id varchar(12),
       PRIMARY KEY (document_id)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    cli()
