from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metrik Tanımları
# 1. Counter: Sürekli artan toplam satılan bilet sayısı
SOLD_TICKETS = Counter('ticket_sold_total', 'Toplam satilan bilet adedi')

# 2. Counter: Tükendiği veya hata oluştuğu için başarısız olan satın alma denemeleri
FAILED_TICKETS = Counter('ticket_failed_total', 'Basarisiz bilet alim denemeleri')

# 3. Gauge: Anlık kalan bilet stoğu (satıldıkça azalır, iade edilirse artabilir)
REMAINING_TICKETS = Gauge('ticket_remaining_stock', 'Depoda anlik kalan bilet sayisi')

# Başlangıç stoğu: 50 adet bilet ile başlatalım
INITIAL_STOCK = 50
REMAINING_TICKETS.set(INITIAL_STOCK)

@app.route('/tickets', methods=['GET'])
def get_tickets():
    """Mevcut kalan bilet sayısını döner"""
    return jsonify({
        "status": "success",
        "remaining_tickets": REMAINING_TICKETS._value.get()
    }), 200

@app.route('/buy', methods=['POST'])
def buy_ticket():
    """1 adet bilet satın alma işlemi"""
    current_stock = REMAINING_TICKETS._value.get()
    
    if current_stock > 0:
        REMAINING_TICKETS.dec(1)  # Gauge değerini 1 azalt
        SOLD_TICKETS.inc()         # Counter değerini 1 artır
        return jsonify({
            "message": "Bilet basariyla alindi!",
            "remaining": REMAINING_TICKETS._value.get()
        }), 200
    else:
        FAILED_TICKETS.inc()       # Başarısız işlem sayacını 1 artır
        return jsonify({
            "error": "Biletler tukendi!"
        }), 400

@app.route('/metrics')
def metrics():
    """Prometheus'un verileri çekeceği endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)