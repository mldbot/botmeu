from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/twiml")
def twiml():
    otp = request.args.get("otp")
    client = request.args.get("client")
    company = request.args.get("company")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">
        Hello {client}, this is {company}. Your one time password is {" ".join(otp)}. Goodbye.
    </Say>
</Response>"""
    return Response(xml, mimetype="application/xml")

if __name__ == "__main__":
    app.run(port=5000)
