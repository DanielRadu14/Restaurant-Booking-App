import mysql.connector
import time
from datetime import date, datetime, timedelta
from mysql.connector import Error
from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

contor_tari = 1
contor_orase = 1
contor_temp = 1

@app.route("/api/countries", methods=["POST"])
def postcountry():
    global contor_tari

    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    nume = payload["nume"]
    latitudine = payload["lat"]
    longitudine = payload["lon"]
    
    if not nume or not latitudine or not longitudine:
        return Response(status=400)
    
    if isinstance(latitudine, str) or isinstance(longitudine, str):
        return Response(status=400)

    try:
        add_country = ("INSERT INTO tari(id, nume_tara, latitudine, longitudine) VALUES (%s, %s, %s, %s)")
        data_country = (contor_tari, nume, latitudine, longitudine)
        cursor.execute(add_country, data_country)
        cursor.execute("COMMIT")

    except Error:
        return Response(status=409)

    contor_tari = contor_tari + 1

    query = ("SELECT id FROM tari WHERE nume_tara = %s")
    cursor.execute(query, (nume,))

    records = cursor.fetchall()

    return jsonify(records), 201

@app.route("/api/countries", methods=["GET"])
def getcountries():
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT * FROM tari")
    cursor.execute(query)

    records = cursor.fetchall()
    return jsonify(records), 200

@app.route("/api/countries/<int:idd>", methods=["PUT"])
def putcountry(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    id_body = payload["id"]
    nume = payload["nume"]
    latitudine = payload["lat"]
    longitudine = payload["lon"]
    
    if not nume or not latitudine or not longitudine or not id_body or idd != id_body:
        return Response(status=400)

    if isinstance(latitudine, str) or isinstance(longitudine, str):
        return Response(status=400)

    query = ("SELECT id FROM tari WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    try:
        query = ("UPDATE tari SET id = %s, nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s")
        cursor.execute(query, (id_body, nume, latitudine, longitudine, idd))
        cursor.execute("COMMIT")
    except Error:
        return Response(status=409)

    return Response(status=200)

@app.route("/api/countries/<int:idd>", methods=["DELETE"])
def deletecountry(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT id FROM tari WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    query = ("SELECT id FROM orase WHERE id_tara = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()

    aux_records = records
    records = []
    for idOras in aux_records:
        query = ("SELECT id from temperaturi WHERE id_oras = %s")
        cursor.execute(query, (idOras[0],))
        records = records + cursor.fetchall()

    for idOras in aux_records:
        query = ("DELETE FROM orase WHERE id = %s")
        cursor.execute(query, (idOras[0],))
        cursor.execute("COMMIT")

    for id_temp in records:
        query = ("DELETE FROM temperaturi WHERE id = %s")
        cursor.execute(query, (id_temp[0],))
        cursor.execute("COMMIT")

    query = ("DELETE FROM tari WHERE id = %s")
    cursor.execute(query, (idd,))
    cursor.execute("COMMIT")

    return Response(status=200)

@app.route("/api/cities", methods=["POST"])
def postcity():
    global contor_orase

    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    idTara = payload["idTara"]
    nume = payload["nume"]
    latitudine = payload["lat"]
    longitudine = payload["lon"]
    
    if not nume or not latitudine or not longitudine or not idTara:
        return Response(status=400)
    
    if isinstance(latitudine, str) or isinstance(longitudine, str) or isinstance(idTara, str):
        return Response(status=400)

    query = ("SELECT id FROM tari WHERE id = %s")
    cursor.execute(query, (idTara,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    try:
        add_city = ("INSERT INTO orase(id, id_tara, nume_oras, latitudine, longitudine) VALUES (%s, %s, %s, %s, %s)")
        data_city = (contor_orase, idTara, nume, latitudine, longitudine)
        cursor.execute(add_city, data_city)
        cursor.execute("COMMIT")

    except Error:
        return Response(status=409)

    contor_orase = contor_orase + 1

    query = ("SELECT id FROM orase WHERE nume_oras = %s and id_tara = %s")
    cursor.execute(query, (nume,idTara))

    records = cursor.fetchall()

    return jsonify(records), 201

@app.route("/api/cities", methods=["GET"])
def getcities():
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT * FROM orase")
    cursor.execute(query)

    records = cursor.fetchall()
    return jsonify(records), 200

@app.route("/api/cities/country/<int:idd>", methods=["GET"])
def getcitiesfromcountry(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT id, nume_oras, latitudine, longitudine FROM orase WHERE id_tara = %s")
    cursor.execute(query, (idd,))

    records = cursor.fetchall()
    return jsonify(records), 200

@app.route("/api/cities/<int:idd>", methods=["PUT"])
def putcity(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    id_body = payload["id"]
    idTara = payload["idTara"]
    nume = payload["nume"]
    latitudine = payload["lat"]
    longitudine = payload["lon"]
    
    if not nume or not latitudine or not longitudine or not id_body or not idTara or idd != id_body:
        return Response(status=400)

    if isinstance(latitudine, str) or isinstance(longitudine, str) or isinstance(idTara, str):
        return Response(status=400)

    query = ("SELECT id FROM orase WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    query = ("SELECT id FROM tari WHERE id = %s")
    cursor.execute(query, (idTara,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    try:
        query = ("UPDATE orase SET id = %s, id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s WHERE id = %s")
        cursor.execute(query, (id_body, idTara, nume, latitudine, longitudine, idd))
        cursor.execute("COMMIT")
    except Error:
        return Response(status=409)

    return Response(status=200)

@app.route("/api/cities/<int:idd>", methods=["DELETE"])
def deletecity(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT id FROM orase WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    query = ("SELECT id FROM temperaturi WHERE id_oras = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()

    for id_temp in records:
        query = ("DELETE FROM temperaturi WHERE id = %s")
        cursor.execute(query, (id_temp[0],))
        cursor.execute("COMMIT")

    query = ("DELETE FROM orase WHERE id = %s")
    cursor.execute(query, (idd,))
    cursor.execute("COMMIT")

    return Response(status=200)

@app.route("/api/temperatures", methods=["POST"])
def posttemperatures():
    global contor_temp

    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    idOras = payload["idOras"]
    valoare = payload["valoare"]
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)

    timestamp = str(timeObj.tm_year) + '-' + str(timeObj.tm_mon) + '-' + str(timeObj.tm_mday) + ' ' + str(timeObj.tm_hour) + ':' + str(timeObj.tm_min) + ':' + str(timeObj.tm_sec) 
    
    if not idOras or not valoare:
        return Response(status=400)
    
    if isinstance(valoare, str) or isinstance(idOras, str):
        return Response(status=400)

    query = ("SELECT id FROM orase WHERE id = %s")
    cursor.execute(query, (idOras,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    try:
        add_temp = ("INSERT INTO temperaturi(id, id_oras, valoare, timestamp) VALUES (%s, %s, %s, %s)")
        data_temp = (contor_temp, idOras, valoare, timestamp)
        cursor.execute(add_temp, data_temp)
        cursor.execute("COMMIT")

    except Error:
        return Response(status=409)

    contor_temp = contor_temp + 1

    query = ("SELECT id FROM temperaturi WHERE timestamp = %s and id_oras = %s")
    cursor.execute(query, (timestamp,idOras))

    records = cursor.fetchall()

    return jsonify(records), 201

@app.route("/api/temperatures", methods=["GET"])
def gettemperatures():
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    latitudine = request.args.get('lat', default = 1, type = float)
    longitudine = request.args.get('lon', default = 1, type = int)
    from_date = request.args.get('from', default = 1, type = str)
    until_date = request.args.get('until', default = 1, type = str)

    records = []
    temp_records = []
    if latitudine != 1 and longitudine == 1:
        query = ("SELECT id from orase WHERE latitudine = %s")
        cursor.execute(query, (latitudine,))
        records = cursor.fetchall()

        aux_records = records
        records = []
        for idOras in aux_records:
            query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
            cursor.execute(query, (idOras[0],))
            records = records + cursor.fetchall()

        if from_date != 1 and until_date == 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

        elif from_date == 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            
        elif from_date != 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            if timestamp_parser[0] == until_date_parser[0]:
                                if timestamp_parser[1] == until_date_parser[1]:
                                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                                elif timestamp_parser[1] <= until_date_parser[1]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[0] <= until_date_parser[0]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]

        else:
            temp_records = records

    elif latitudine == 1 and longitudine != 1:
        query = ("SELECT id from orase WHERE longitudine = %s")
        cursor.execute(query, (longitudine,))
        records = cursor.fetchall()

        aux_records = records
        records = []
        for idOras in aux_records:
            query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
            cursor.execute(query, (idOras[0],))
            records = records + cursor.fetchall()

        if from_date != 1 and until_date == 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

        elif from_date == 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            
        elif from_date != 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            if timestamp_parser[0] == until_date_parser[0]:
                                if timestamp_parser[1] == until_date_parser[1]:
                                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                                elif timestamp_parser[1] <= until_date_parser[1]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[0] <= until_date_parser[0]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
            
        else:
            temp_records = records

    elif latitudine != 1 and longitudine != 1:
        query = ("SELECT id from orase WHERE longitudine = %s and latitudine = %s")
        cursor.execute(query, (longitudine,latitudine))
        records = cursor.fetchall()

        aux_records = records
        records = []
        for idOras in aux_records:
            query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
            cursor.execute(query, (idOras[0],))
            records = records + cursor.fetchall()

        if from_date != 1 and until_date == 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

        elif from_date == 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            
        elif from_date != 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            if timestamp_parser[0] == until_date_parser[0]:
                                if timestamp_parser[1] == until_date_parser[1]:
                                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                                elif timestamp_parser[1] <= until_date_parser[1]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[0] <= until_date_parser[0]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
            
        else:
            temp_records = records

    else:
        query = ("SELECT id from orase")
        cursor.execute(query)
        records = cursor.fetchall()

        aux_records = records
        records = []
        for idOras in aux_records:
            query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
            cursor.execute(query, (idOras[0],))
            records = records + cursor.fetchall()

        if from_date != 1 and until_date == 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

        elif from_date == 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

        elif from_date != 1 and until_date != 1:

            for (id_temp, valoare, timestamp) in records:
                timestamp_parser = timestamp.split('-')
                from_date_parser = from_date.split('-')
                until_date_parser = until_date.split('-')

                if timestamp_parser[0] == from_date_parser[0]:
                    if timestamp_parser[1] == from_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                            if timestamp_parser[0] == until_date_parser[0]:
                                if timestamp_parser[1] == until_date_parser[1]:
                                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                                elif timestamp_parser[1] <= until_date_parser[1]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[0] <= until_date_parser[0]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] >= from_date_parser[1]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] >= from_date_parser[0]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]

        else:
            temp_records = records
    
    return jsonify(temp_records), 200

@app.route("/api/temperatures/cities/<int:idd>", methods=["GET"])
def gettemperaturesfromcity(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    from_date = request.args.get('from', default = 1, type = str)
    until_date = request.args.get('until', default = 1, type = str)

    query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()

    temp_records = []
    if from_date != 1 and until_date == 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            from_date_parser = from_date.split('-')

            if timestamp_parser[0] == from_date_parser[0]:
                if timestamp_parser[1] == from_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] >= from_date_parser[1]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] >= from_date_parser[0]:
                temp_records = temp_records + [[id_temp, valoare, timestamp]]

    elif from_date == 1 and until_date != 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            until_date_parser = until_date.split('-')

            if timestamp_parser[0] == until_date_parser[0]:
                if timestamp_parser[1] == until_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] <= until_date_parser[1]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] <= until_date_parser[0]:
                temp_records = temp_records + [[id_temp, valoare, timestamp]]

    elif from_date != 1 and until_date != 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            from_date_parser = from_date.split('-')
            until_date_parser = until_date.split('-')

            if timestamp_parser[0] == from_date_parser[0]:
                if timestamp_parser[1] == from_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] >= from_date_parser[1]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] >= from_date_parser[0]:
                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

    else:
        temp_records = records

    return jsonify(temp_records), 200

@app.route("/api/temperatures/countries/<int:idd>", methods=["GET"])
def gettemperaturesfromcountry(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    from_date = request.args.get('from', default = 1, type = str)
    until_date = request.args.get('until', default = 1, type = str)

    query = ("SELECT id from orase WHERE id_tara = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()

    aux_records = records
    records = []
    for idOras in aux_records:
        query = ("SELECT id, valoare, timestamp from temperaturi WHERE id_oras = %s")
        cursor.execute(query, (idOras[0],))
        records = records + cursor.fetchall()

    temp_records = []
    if from_date != 1 and until_date == 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            from_date_parser = from_date.split('-')

            if timestamp_parser[0] == from_date_parser[0]:
                if timestamp_parser[1] == from_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] >= from_date_parser[1]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] >= from_date_parser[0]:
                temp_records = temp_records + [[id_temp, valoare, timestamp]]

    elif from_date == 1 and until_date != 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            until_date_parser = until_date.split('-')

            if timestamp_parser[0] == until_date_parser[0]:
                if timestamp_parser[1] == until_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] <= until_date_parser[1]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] <= until_date_parser[0]:
                temp_records = temp_records + [[id_temp, valoare, timestamp]]

    elif from_date != 1 and until_date != 1:

        for (id_temp, valoare, timestamp) in records:
            timestamp_parser = timestamp.split('-')
            from_date_parser = from_date.split('-')
            until_date_parser = until_date.split('-')

            if timestamp_parser[0] == from_date_parser[0]:
                if timestamp_parser[1] == from_date_parser[1]:
                    if timestamp_parser[2].split(' ')[0] >= from_date_parser[2]:
                        if timestamp_parser[0] == until_date_parser[0]:
                            if timestamp_parser[1] == until_date_parser[1]:
                                if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                    temp_records = temp_records + [[id_temp, valoare, timestamp]]
                            elif timestamp_parser[1] <= until_date_parser[1]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[0] <= until_date_parser[0]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[1] >= from_date_parser[1]:
                    if timestamp_parser[0] == until_date_parser[0]:
                        if timestamp_parser[1] == until_date_parser[1]:
                            if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                                temp_records = temp_records + [[id_temp, valoare, timestamp]]
                        elif timestamp_parser[1] <= until_date_parser[1]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[0] <= until_date_parser[0]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
            elif timestamp_parser[0] >= from_date_parser[0]:
                if timestamp_parser[0] == until_date_parser[0]:
                    if timestamp_parser[1] == until_date_parser[1]:
                        if timestamp_parser[2].split(' ')[0] <= until_date_parser[2]:
                            temp_records = temp_records + [[id_temp, valoare, timestamp]]
                    elif timestamp_parser[1] <= until_date_parser[1]:
                        temp_records = temp_records + [[id_temp, valoare, timestamp]]
                elif timestamp_parser[0] <= until_date_parser[0]:
                    temp_records = temp_records + [[id_temp, valoare, timestamp]]

    else:
        temp_records = records

    return jsonify(temp_records), 200

@app.route("/api/temperatures/<int:idd>", methods=["PUT"])
def puttemperature(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    payload  = request.get_json(silent=True)

    if not payload:
         return Response(status=400)
    
    id_body = payload["id"]
    idOras = payload["idOras"]
    valoare = payload["valoare"]
    
    if not id_body or not idOras or not valoare or idd != id_body:
        return Response(status=400)

    if isinstance(valoare, str) or isinstance(idOras, str):
        return Response(status=400)

    query = ("SELECT id FROM temperaturi WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    query = ("SELECT id FROM orase WHERE id = %s")
    cursor.execute(query, (idOras,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    try:
        query = ("UPDATE temperaturi SET id = %s, id_oras = %s, valoare = %s WHERE id = %s")
        cursor.execute(query, (id_body, idOras, valoare, idd))
        cursor.execute("COMMIT")
    except Error:
        return Response(status=409)

    return Response(status=200)

@app.route("/api/temperatures/<int:idd>", methods=["DELETE"])
def deletetemperatures(idd):
    connection = mysql.connector.connect(host='some-mysql',
                                         database='meteo',
                                         user='root',
                                         password = 'daniel')
    cursor = connection.cursor()

    query = ("SELECT id FROM temperaturi WHERE id = %s")
    cursor.execute(query, (idd,))
    records = cursor.fetchall()
    
    if len(records) == 0:
        return Response(status=404)

    query = ("DELETE FROM temperaturi WHERE id = %s")
    cursor.execute(query, (idd,))
    cursor.execute("COMMIT")

    return Response(status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
