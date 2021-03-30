#!/usr/bin/env python
import argparse
import json
import sys
import unittest.mock
import urllib.request
import webbrowser
import time


CITIES = [
   'ABILENE', 'ALAMO', 'ALICE', 'ARANSAS PASS', 'AUSTIN', 'Austin', 'BASTROP',
   'BAY CITY', 'BAYTOWN', 'BEAUMONT', 'BEE CAVE', 'BEEVILLE', 'BELLAIRE', 'BELLMEAD',
   'BELTON', 'BIG SPRING', 'BOERNE', 'BRENHAM', 'BROWNSVILLE', 'BRYAN', 'BUDA',
   'BURLESON', 'BURNET', 'Burleson', 'CARRIZO SPRINGS', 'CEDAR PARK', 'CLEBURNE', 'COLLEGE STATION',
   'CONROE', 'COPPERAS COVE', 'CORPUS CHRISTI', 'CORSICANA', 'CUERO', 'CYPRESS', 'Corpus Christi',
   'DEER PARK', 'DEL RIO', 'DRIPPING SPRINGS', 'EAGLE PASS', 'EDINBURG', 'EDNA', 'EL CAMPO',
   'ELGIN', 'ELSA', 'ENNIS', 'FALFURRIAS', 'FLORESVILLE', 'FREDERICKSBURG', 'FRIENDSWOOD',
   'GATESVILLE', 'GEORGETOWN', 'GONZALES', 'GRANBURY', 'HARKER HEIGHTS', 'HARLINGEN', 'HONDO',
   'HOUSTON', 'HUDSON OAKS', 'HUMBLE', 'HUNTSVILLE', 'HUTTO', 'KATY', 'KENEDY',
   'KERRVILLE', 'KILLEEN', 'KINGSVILLE', 'KINGWOOD', 'KYLE', 'Kerrville', 'Killeen',
   'LA GRANGE', 'LA VERNIA', 'LAKE JACKSON', 'LAKEWAY', 'LAREDO', 'LEAGUE CITY', 'LEANDER',
   'LOCKHART', 'LUBBOCK', 'LYTLE', 'MAGNOLIA', 'MARBLE FALLS', 'MCALLEN', 'MEXIA',
   'MIDLAND', 'MISSION', 'MISSOURI CITY', 'MONT BELVIEU', 'NEW BRAUNFELS', 'ODESSA', 'PALMHURST',
   'PALMVIEW', 'PASADENA', 'PEARLAND', 'PEARSALL', 'PFLUGERVILLE', 'PHARR', 'PLEASANTON',
   'PORT ARTHUR', 'PORT LAVACA', 'PORTLAND', 'RICHMOND', 'RIO GRANDE CITY', 'ROCKPORT', 'ROUND ROCK',
   'SAN ANGELO', 'SAN ANTONIO', 'SAN BENITO', 'SAN JUAN', 'SAN MARCOS', 'SCHERTZ', 'SEGUIN',
   'SPRING BRANCH', 'SPRING', 'STEPHENVILLE', 'SUGAR LAND', 'San Antonio', 'TAYLOR', 'TEMPLE',
   'TEXAS CITY', 'THE WOODLANDS', 'TOMBALL', 'Tomball', 'UNIVERSAL CITY', 'UVALDE', 'VICTORIA',
   'WACO', 'WAXAHACHIE', 'WESLACO', 'WEST LAKE HILLS', 'WHARTON', 'WIMBERLEY', 'WOODWAY',
   'Waco', 'Waxahachie',
]

def main(locations, manufacturers,):
    locations = list(map(lambda x: x.lower(), locations))
    manufacturers = list(map(lambda x: x.lower(), manufacturers))
    req = urllib.request.Request(
        url='https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json',
        headers={
            'authority': 'heb-ecom-covid-vaccine.hebdigital-prd.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'accept': '*/*',
            'origin': 'https://vaccine.heb.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://vaccine.heb.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
    )
    x = 1
    while 1 == 1:
        data = json.load(urllib.request.urlopen(req))
        for location in data['locations']:
            if location['url']:
                if location['city'].lower() not in locations:
                    continue
                for slot in location['slotDetails']:
                    if slot['manufacturer'].lower() in manufacturers:
                        print('Vaccine Found')
                        webbrowser.open(location['url'])
                        input('Press enter to continue')
        print('Checked areas {} times.'.format(x))
        x += 1
        time.sleep(3)

class TestVaccineGetter(unittest.TestCase):
    def setUp(self):
        fh_ = open('vaccine.json', 'r')
        mock_requests = unittest.mock.patch('urllib.request.urlopen', return_value=fh_)

        mock_webbrowser = unittest.mock.patch('webbrowser.open')

        mock_requests.start()
        self.patch = mock_webbrowser.start()

        # mock input so that tests dont require input
        global input
        input = unittest.mock.MagicMock()

        self.addCleanup(mock_requests.stop)
        self.addCleanup(fh_.close)
        self.addCleanup(mock_webbrowser.stop)


    def test_getting_slot(self):
        main(['seguin'], ['pfizer'])
        self.patch.assert_called_once()

    def test_getting_slot_with_moderna(self):
        main(['conroe'], ['moderna'])
        self.patch.assert_called_once()

    def test_getting_no_slots(self):
        main(['san antonio'], ['moderna'])
        self.patch.assert_not_called()



if __name__ == '__main__':
    parser = argparse.ArgumentParser('help find vaccination openings')
    parser.add_argument(
        '--location', '-l', action='append', help='Location that you can get too',
        choices=CITIES,
    )
    parser.add_argument(
        '--manufacturer', '-m', action='append', choices=['Pfizer', 'Moderna'],
        help='Which vaccines manufacturers are you looking for',
    )
    parser.add_argument(
        '--test', '-t', action='store_true',
        help='Test this script',
    )
    args = parser.parse_args()

    if args.test is True:
        sys.argv = sys.argv[:1]
        unittest.main()
    elif args.location and args.manufacturer:
        main(args.location, args.manufacturer)
    else:
        raise Exception('location and manufacturer must be specified')
