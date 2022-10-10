import os

import CloudFlare
from dotenv import load_dotenv
from requests import get

#Load Cloudflare API token
load_dotenv()
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')

def main():
    cf = CloudFlare.CloudFlare(token=CLOUDFLARE_API_TOKEN)
    zones = cf.zones.get(params={"name": "cameronray.co.za"})
    zone_id = zones[0]["id"]
    a_record = cf.zones.dns_records.get(zone_id, params={"name": "rpi-microscope.cameronray.co.za", "type": "A"})[0] 
    a_record["ttl"] = 60
    ip = get('https://api.ipify.org').content.decode('utf8')
    a_record["content"] = ip
    cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)

if __name__ == '__main__':
    main()
