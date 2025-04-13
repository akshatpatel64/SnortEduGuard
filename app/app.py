from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask import Response
from smart_filter import filter_alerts
from summarizer import summarize_alert

import json

app = Flask(__name__)
app.secret_key = 'supersecurebitcampkey'  # used for session tracking
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    with open('../parsed_alerts.json') as f:
        alerts = json.load(f)

    return render_template('index.html', alerts=alerts)


@app.route('/api/alerts')
def api_alerts():
    with open('../parsed_alerts.json') as f:
        return jsonify(json.load(f))
from flask import Response

@app.route('/download-csv')
def download_csv():
    import csv
    from io import StringIO

    with open('../parsed_alerts.json') as f:
        alerts = json.load(f)

    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=[
        'timestamp_iso', 'msg', 'sid', 'priority', 'protocol', 'src', 'dst'
    ])
    writer.writeheader()

    for alert in alerts:
        writer.writerow({
            'timestamp_iso': alert.get('timestamp_iso'),
            'msg': alert.get('msg'),
            'sid': alert.get('sid'),
            'priority': alert.get('priority'),
            'protocol': alert.get('protocol'),
            'src': alert.get('src'),
            'dst': alert.get('dst')
        })

    csv_buffer.seek(0)
    return Response(
        csv_buffer,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=Summary_Alerts_by-AkshatDP.csv"}
    )

@app.route('/download-pdf')
def download_pdf():
    from xhtml2pdf import pisa
    from jinja2 import Template
    from io import BytesIO

    try:
        with open('../parsed_alerts.json') as f:
            alerts = json.load(f)

        html_template = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    padding: 20px;
                    color: #333;
                }
                h1 {
                    font-size: 22px;
                    text-align: center;
                    margin-bottom: 5px;
                }
                .subheader {
                    text-align: center;
                    font-size: 14px;
                    margin-bottom: 15px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }
                th, td {
                    border: 1px solid #ccc;
                    padding: 6px;
                    text-align: left;
                    vertical-align: top;
                    word-break: break-word;
		    white-space: pre-wrap;

                }
                th {
                    background-color: #f8f8f8;
                }
                .footer {
                    margin-top: 30px;
                    text-align: center;
                    font-size: 12px;
                }
                a {
                    color: #007BFF;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <h1>Snort IDS Alert Report</h1>
            <div class="subheader">
                Bitcamp 2025 • University of Maryland<br>
                Prepared by <strong>Akshat D. Patel</strong><br>
                <a href="https://akshatpatel64.github.io/">Visit My Portfolio</a>
            </div>

            <p><strong>Total Alerts:</strong> {{ alerts|length }}</p>

            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Message</th>
                        <th>SID</th>
                        <th>Priority</th>
                        <th>Protocol</th>
                        <th>Source</th>
                        <th>Destination</th>
                    </tr>
                </thead>
                <tbody>
                {% for alert in alerts %}
                    <tr>
                        <td>{{ alert.timestamp_iso }}</td>
                        <td>{{ alert.msg }}</td>
                        <td>{{ alert.sid }}</td>
                        <td>{{ alert.priority }}</td>
                        <td>{{ alert.protocol }}</td>
                        <td>{{ alert.src }}</td>
                        <td>{{ alert.dst }}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>

            <div class="footer">
                This report was generated automatically using Snort IDS on macOS.<br>
                For support, contact: akshatpatel64@umd.edu
            </div>
        </body>
        </html>
        """

        rendered = Template(html_template).render(alerts=alerts)

        pdf_buffer = BytesIO()
        pisa.CreatePDF(rendered, dest=pdf_buffer)
        pdf_buffer.seek(0)

        return Response(pdf_buffer.read(), mimetype='application/pdf', headers={
            'Content-Disposition': 'attachment; filename=alerts_report_By_AkshatDP.pdf'
        })

    except Exception as e:
        print("[❌] Exception during PDF generation:", e)
        return f"Error generating PDF: {e}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'instructor' and password == 'bitcamp2025':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
   

@app.route('/smart-search', methods=['GET', 'POST'])
def smart_search():
    query = ""
    summaries = []

    if request.method == 'POST':
        query = request.form['query']
        print("[+] Received Query:", query)

        # Run your filter engine
        filtered_alerts = filter_alerts(query)

        # Summarize each alert
        summaries = [summarize_alert(alert) for alert in filtered_alerts]

    return render_template('smart_search.html', query=query, summaries=summaries)



if __name__ == '__main__':
    app.run(debug=True)

