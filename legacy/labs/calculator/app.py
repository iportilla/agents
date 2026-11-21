from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def get_primes(n):
    """
    Returns a list of prime numbers up to n using an optimized algorithm.
    """
    if n < 2:
        return []
    
    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

@app.route('/')
def index():
    """Render the home page with the calculator form."""
    return render_template('index.html')

@app.route('/api/primes', methods=['GET'])
def api_primes():
    """
    API endpoint to get prime numbers.
    Query parameter: n (the upper limit)
    Returns JSON with list of primes and metadata.
    """
    try:
        n = request.args.get('n', type=int)
        if n is None:
            return jsonify({'error': 'Missing parameter: n'}), 400
        if n < 2:
            return jsonify({'error': 'Parameter n must be at least 2'}), 400
        
        primes = get_primes(n)
        return jsonify({
            'limit': n,
            'count': len(primes),
            'primes': primes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    POST endpoint to calculate primes.
    Expects JSON with 'n' field.
    """
    try:
        data = request.get_json()
        n = data.get('n')
        
        if n is None:
            return jsonify({'error': 'Missing parameter: n'}), 400
        if not isinstance(n, int):
            return jsonify({'error': 'Parameter n must be an integer'}), 400
        if n < 2:
            return jsonify({'error': 'Parameter n must be at least 2'}), 400
        
        primes = get_primes(n)
        return jsonify({
            'limit': n,
            'count': len(primes),
            'primes': primes,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
