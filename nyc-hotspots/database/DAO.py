from database.DB_connect import DBConnect
from model.location import Location


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProvider():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT Provider
                      FROM nyc_wifi_hotspot_locations 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Provider"])

        cursor.close()
        conn.close()
        return result

    # per prendere solo nodi e poi archi nel modo 1
    @staticmethod
    def getAllLocations(provider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT Location
                          FROM nyc_wifi_hotspot_locations 
                          WHERE Provider = %s
                    """

        cursor.execute(query, (provider, ))

        for row in cursor:
            result.append(row["Location"])

        cursor.close()
        conn.close()
        return result

    # per prendere solo nodi e poi archi nel modo 1
    @staticmethod
    def getAllEdges(provider):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT n1.Location as n1Loc, n2.Location as n2Loc , avg(n2.Latitude) as n2Lat , 
                    AVG(n2.Longitude) as n2Long, avg(n1.Latitude) as n1Lat, avg(n1.Longitude) as n1Long
                            FROM nyc_wifi_hotspot_locations n1, nyc_wifi_hotspot_locations n2
                            WHERE n1.Provider = n2.Provider 
                            AND n2.Provider = %s
                            AND n1.Location < n2.Location 
                            GROUP BY n1.Location, n2.Location 
                    """  #penultima riga per assicurarmi di non prendere due volte la riga aB e BA
            cursor.execute(query, (provider,))
            for row in cursor:
                loc1 = Location(row["n1Loc"], row["n1Lat"], row["n1Long"])
                loc2 = Location(row["n2Loc"], row["n2Lat"], row["n2Long"])
                result.append((loc1, loc2))
            cursor.close()
            cnx.close()
            return result

    # per prendere archi nel modo 2
    @staticmethod
    def getLocationsOfProviderV2(provider):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT Location , AVG(nwhl.Latitude) as lat , avg(nwhl.Longitude) as lon
                        FROM nyc_wifi_hotspot_locations nwhl 
                        WHERE Provider = %s
                        GROUP BY Location 
                        ORDER BY Location ASC 
                    """
            cursor.execute(query, (provider,))
            for row in cursor:
                result.append(Location(row["Location"], row["lat"], row["lon"]))

            cursor.close()
            cnx.close()
            return result