
from flask import Flask, request, Blueprint, render_template, jsonify
from flask_restful import Resource, Api
import yfinance as yf
import pandas as pd
from .predictor import fetch_stock_data

a = Blueprint('app', __name__)

@a.route('/')
def home():
    return render_template("home.html")


@a.route('/select_industry')
def home():
    return render_template("industry.html")


@a.route('/stock_data', methods = ["POST"])
def post():
    # Parse request parameters
    symbol = request.form.get('symbol', default=None, type=str)
    start_date = request.form.get('start_date', default=None, type=str)
    end_date = request.form.get('end_date', default=None, type=str)
    
    # Validate input parameters
    if not symbol  or not start_date or not end_date:
        return jsonify({"error": "Missing required parameters"})
                
    # Fetch stock data
    try:
        result = fetch_stock_data(symbol, start_date, end_date)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return  jsonify({"symbol": symbol, "data": result})
    