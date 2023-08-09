{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNbETAX49f/17tRpWnnyF77"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import requests\n",
        "import yfinance as yf\n",
        "import ta\n",
        "import plotly.graph_objs as go\n",
        "\n",
        "ALPHA_VANTAGE_API_KEY = \"1OOTZYOVHIYXH2BZ\"\n",
        "\n",
        "def get_live_data(symbol):\n",
        "    url = f\"https://www.alphavantage.co/query\"\n",
        "    params = {\n",
        "        \"function\": \"GLOBAL_QUOTE\",\n",
        "        \"symbol\": symbol,\n",
        "        \"apikey\": ALPHA_VANTAGE_API_KEY\n",
        "    }\n",
        "\n",
        "    response = requests.get(url, params=params)\n",
        "    data = response.json()\n",
        "\n",
        "    if \"Global Quote\" in data:\n",
        "        return data[\"Global Quote\"]\n",
        "    else:\n",
        "        st.error(\"Error fetching data.\")\n",
        "        return None\n",
        "\n",
        "def get_company_name(symbol):\n",
        "    company = yf.Ticker(symbol)\n",
        "    info = company.info\n",
        "    if 'longName' in info:\n",
        "        return info['longName']\n",
        "    return None\n",
        "\n",
        "def get_historical_data(symbol, start_date, end_date):\n",
        "    df = yf.download(symbol, start=start_date, end=end_date)\n",
        "    return df\n",
        "\n",
        "# Rest of the functions remain the same\n",
        "\n",
        "def generate_area_chart(df):\n",
        "    fig = go.Figure(data=[\n",
        "        go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Price'),\n",
        "        go.Scatter(x=df.index, y=df['bb_upper'], fill='tonexty', mode='lines', name='Bollinger Upper', line=dict(width=0)),\n",
        "        go.Scatter(x=df.index, y=df['bb_lower'], fill='tonexty', mode='lines', name='Bollinger Lower', line=dict(width=0))\n",
        "    ])\n",
        "    fig.update_layout(title='Area Chart with Bollinger Bands', yaxis_title='Price')\n",
        "    st.plotly_chart(fig)\n",
        "\n",
        "def generate_technical_recommendations(df):\n",
        "    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()\n",
        "    df['rsi_signal'] = 'Neutral'\n",
        "    df.loc[df['rsi'] < 30, 'rsi_signal'] = 'Buy'\n",
        "    df.loc[df['rsi'] > 70, 'rsi_signal'] = 'Sell'\n",
        "\n",
        "    st.write(\"\\nTechnical Recommendations based on RSI:\")\n",
        "    st.write(\"--------------------------------------\")\n",
        "    for index, row in df.iterrows():\n",
        "        st.write(f\"Date: {index.date()}, RSI: {row['rsi']:.2f}, Recommendation: {row['rsi_signal']}\")\n",
        "\n",
        "def main():\n",
        "    st.title(\"Stock Analysis/Recommendation Software\")\n",
        "    st.write(\"----------------------------------------------\")\n",
        "\n",
        "    stock_symbol = st.text_input(\"Enter the stock symbol:\")\n",
        "    if st.button(\"Fetch Data\"):\n",
        "        live_data = get_live_data(stock_symbol)\n",
        "\n",
        "        if live_data:\n",
        "            st.write(\"\\nLive Stock Information:\")\n",
        "            st.write(\"-----------------------\")\n",
        "            st.write(\"Symbol:\", live_data[\"01. symbol\"])\n",
        "            st.write(\"Company Name:\", get_company_name(stock_symbol))  # Display the company name\n",
        "            st.write(\"Open:\", live_data[\"02. open\"])\n",
        "            st.write(\"High:\", live_data[\"03. high\"])\n",
        "            st.write(\"Low:\", live_data[\"04. low\"])\n",
        "            st.write(\"Price:\", live_data[\"05. price\"])\n",
        "            st.write(\"Volume:\", live_data[\"06. volume\"])\n",
        "            st.write(\"Latest Trading Day:\", live_data[\"07. latest trading day\"])\n",
        "            st.write(\"Previous Close:\", live_data[\"08. previous close\"])\n",
        "\n",
        "            start_date = \"2023-01-01\"\n",
        "            end_date = \"2023-08-01\"\n",
        "            historical_data = get_historical_data(stock_symbol, start_date, end_date)\n",
        "\n",
        "            generate_candlestick_chart(historical_data)\n",
        "            generate_rsi_with_reversal(historical_data)\n",
        "            generate_bollinger_bands(historical_data)\n",
        "            generate_area_chart(historical_data)\n",
        "            generate_technical_recommendations(historical_data)\n",
        "\n",
        "        else:\n",
        "            st.error(\"Failed to fetch live stock information.\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()\n",
        "\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gB5Vi9OAhEP7",
        "outputId": "b17c4140-c38b-4e7c-8e45-e5e31024a43a"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2023-08-09 05:46:02.995 \n",
            "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
            "  command:\n",
            "\n",
            "    streamlit run /usr/local/lib/python3.10/dist-packages/ipykernel_launcher.py [ARGUMENTS]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit"
      ],
      "metadata": {
        "id": "ivWMNsgN0xIA"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install requests mplfinance yfinance ta\n"
      ],
      "metadata": {
        "id": "d8MLx0pduMPW"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}