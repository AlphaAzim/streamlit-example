{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNMdNSDnqTLtAJbOfpF4nj0",
      "include_colab_link": true
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
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/AlphaAzim/streamlit-example/blob/master/Stock_py.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import yfinance as yf\n",
        "import plotly.graph_objects as go\n",
        "import pandas as pd\n",
        "import talib\n",
        "import streamlit as st\n",
        "\n",
        "def get_realtime_data(ticker_symbols):\n",
        "    stock_data = {}\n",
        "    for symbol in ticker_symbols:\n",
        "        stock = yf.Ticker(symbol)\n",
        "        info = stock.info\n",
        "\n",
        "        stock_data[symbol] = {\n",
        "            \"Price\": info.get(\"regularMarketPrice\", \"N/A\"),\n",
        "            \"EPS\": info.get(\"trailingEps\", \"N/A\"),\n",
        "            \"PE Ratio\": info.get(\"trailingPE\", \"N/A\"),\n",
        "            \"Profit\": info.get(\"profitMargins\", \"N/A\"),\n",
        "            \"Market Cap\": info.get(\"marketCap\", \"N/A\"),\n",
        "            \"Bid\": info.get(\"bid\", \"N/A\"),\n",
        "            \"Ask\": info.get(\"ask\", \"N/A\"),\n",
        "            \"Open\": info.get(\"regularMarketOpen\", \"N/A\"),\n",
        "            \"Close\": info.get(\"regularMarketPreviousClose\", \"N/A\"),\n",
        "            \"Volume\": info.get(\"regularMarketVolume\", \"N/A\"),\n",
        "            \"Avg Volume\": info.get(\"averageDailyVolume10Day\", \"N/A\"),\n",
        "            \"52 Week High\": info.get(\"fiftyTwoWeekHigh\", \"N/A\"),\n",
        "            \"52 Week Low\": info.get(\"fiftyTwoWeekLow\", \"N/A\"),\n",
        "        }\n",
        "\n",
        "    return stock_data\n",
        "\n",
        "def plot_candlestick_graph(df, symbol):\n",
        "    fig = go.Figure(data=[go.Candlestick(x=df.index,\n",
        "                                         open=df['Open'],\n",
        "                                         high=df['High'],\n",
        "                                         low=df['Low'],\n",
        "                                         close=df['Close'])])\n",
        "\n",
        "    fig.update_layout(\n",
        "        title=f\"{symbol} Candlestick Chart\",\n",
        "        xaxis_title=\"Time\",\n",
        "        yaxis_title=\"Price (USD)\",\n",
        "        template=\"plotly_white\"\n",
        "    )\n",
        "\n",
        "    st.plotly_chart(fig)\n",
        "\n",
        "def plot_technical_indicators(df, symbol):\n",
        "    df[\"EMA\"] = talib.EMA(df[\"Close\"], timeperiod=20)\n",
        "    df[\"SMA\"] = talib.SMA(df[\"Close\"], timeperiod=50)\n",
        "    df[\"RSI\"] = talib.RSI(df[\"Close\"])\n",
        "    df[\"MACD\"], _, _ = talib.MACD(df[\"Close\"])\n",
        "\n",
        "    fig = go.Figure()\n",
        "    fig.add_trace(go.Scatter(x=df.index, y=df[\"EMA\"], name=\"20-day EMA\", line=dict(color=\"blue\")))\n",
        "    fig.add_trace(go.Scatter(x=df.index, y=df[\"SMA\"], name=\"50-day SMA\", line=dict(color=\"red\")))\n",
        "    fig.add_trace(go.Scatter(x=df.index, y=df[\"RSI\"], name=\"RSI\", line=dict(color=\"green\")))\n",
        "    fig.add_trace(go.Scatter(x=df.index, y=df[\"MACD\"], name=\"MACD\", line=dict(color=\"purple\")))\n",
        "\n",
        "    fig.update_layout(\n",
        "        title=f\"{symbol} Technical Indicators\",\n",
        "        xaxis_title=\"Time\",\n",
        "        template=\"plotly_white\"\n",
        "    )\n",
        "\n",
        "    st.plotly_chart(fig)\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    try:\n",
        "        user_input = input(\"Enter stock symbols (comma-separated): \")\n",
        "        nyse_ticker_symbols = [symbol.strip().upper() for symbol in user_input.split(\",\")]\n",
        "        realtime_data = get_realtime_data(nyse_ticker_symbols)\n",
        "\n",
        "        # Display real-time data in a table format\n",
        "        st.title(\"Real-Time Stock Data\")\n",
        "        df_realtime_data = pd.DataFrame(realtime_data).T\n",
        "        st.dataframe(df_realtime_data)\n",
        "\n",
        "        for symbol, data in realtime_data.items():\n",
        "            st.write(f\"\\n{symbol} Real-Time Data:\")\n",
        "            for key, value in data.items():\n",
        "                st.write(f\"{key}: {value}\")\n",
        "\n",
        "            # Fetch historical data for candlestick chart\n",
        "            stock = yf.Ticker(symbol)\n",
        "            df = stock.history(period=\"1mo\", interval=\"1d\")  # You can adjust the period as per your requirement\n",
        "            plot_candlestick_graph(df, symbol)\n",
        "\n",
        "            # Plot technical indicators\n",
        "            plot_technical_indicators(df, symbol)\n",
        "\n",
        "    except Exception as e:\n",
        "        st.error(f\"Error fetching real-time data: {e}\")\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DPAWjQYBihXH",
        "outputId": "dd2836d6-f3f0-4529-ab15-f870f9dfab7a"
      },
      "execution_count": 21,
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Enter stock symbols (comma-separated): AAPL\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2023-08-04 12:49:27.483 \n",
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
        "pip install streamlit\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8ftNRQJkl-NH",
        "outputId": "7f3ee201-a2a1-4a69-e8e1-edfd79b6bc06"
      },
      "execution_count": 20,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting streamlit\n",
            "  Downloading streamlit-1.25.0-py2.py3-none-any.whl (8.1 MB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m8.1/8.1 MB\u001b[0m \u001b[31m50.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: altair<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.2.2)\n",
            "Requirement already satisfied: blinker<2,>=1.0.0 in /usr/lib/python3/dist-packages (from streamlit) (1.4)\n",
            "Requirement already satisfied: cachetools<6,>=4.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (5.3.1)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (8.1.6)\n",
            "Requirement already satisfied: importlib-metadata<7,>=1.4 in /usr/lib/python3/dist-packages (from streamlit) (4.6.4)\n",
            "Requirement already satisfied: numpy<2,>=1.19.3 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.22.4)\n",
            "Requirement already satisfied: packaging<24,>=16.8 in /usr/local/lib/python3.10/dist-packages (from streamlit) (23.1)\n",
            "Requirement already satisfied: pandas<3,>=1.3.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (1.5.3)\n",
            "Requirement already satisfied: pillow<10,>=7.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (9.4.0)\n",
            "Requirement already satisfied: protobuf<5,>=3.20 in /usr/local/lib/python3.10/dist-packages (from streamlit) (3.20.3)\n",
            "Requirement already satisfied: pyarrow>=6.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (9.0.0)\n",
            "Collecting pympler<2,>=0.9 (from streamlit)\n",
            "  Downloading Pympler-1.0.1-py3-none-any.whl (164 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m164.8/164.8 kB\u001b[0m \u001b[31m23.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: python-dateutil<3,>=2.7.3 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.8.2)\n",
            "Requirement already satisfied: requests<3,>=2.18 in /usr/local/lib/python3.10/dist-packages (from streamlit) (2.27.1)\n",
            "Requirement already satisfied: rich<14,>=10.14.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (13.4.2)\n",
            "Requirement already satisfied: tenacity<9,>=8.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (8.2.2)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.10/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.1.0 in /usr/local/lib/python3.10/dist-packages (from streamlit) (4.7.1)\n",
            "Collecting tzlocal<5,>=1.1 (from streamlit)\n",
            "  Downloading tzlocal-4.3.1-py3-none-any.whl (20 kB)\n",
            "Collecting validators<1,>=0.2 (from streamlit)\n",
            "  Downloading validators-0.20.0.tar.gz (30 kB)\n",
            "  Preparing metadata (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
            "Collecting gitpython!=3.1.19,<4,>=3.0.7 (from streamlit)\n",
            "  Downloading GitPython-3.1.32-py3-none-any.whl (188 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m188.5/188.5 kB\u001b[0m \u001b[31m23.8 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hCollecting pydeck<1,>=0.8 (from streamlit)\n",
            "  Downloading pydeck-0.8.0-py2.py3-none-any.whl (4.7 MB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m4.7/4.7 MB\u001b[0m \u001b[31m86.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: tornado<7,>=6.0.3 in /usr/local/lib/python3.10/dist-packages (from streamlit) (6.3.1)\n",
            "Collecting watchdog>=2.1.5 (from streamlit)\n",
            "  Downloading watchdog-3.0.0-py3-none-manylinux2014_x86_64.whl (82 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m82.1/82.1 kB\u001b[0m \u001b[31m12.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: entrypoints in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.4)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (3.1.2)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (4.3.3)\n",
            "Requirement already satisfied: toolz in /usr/local/lib/python3.10/dist-packages (from altair<6,>=4.0->streamlit) (0.12.0)\n",
            "Collecting gitdb<5,>=4.0.1 (from gitpython!=3.1.19,<4,>=3.0.7->streamlit)\n",
            "  Downloading gitdb-4.0.10-py3-none-any.whl (62 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m62.7/62.7 kB\u001b[0m \u001b[31m8.8 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas<3,>=1.3.0->streamlit) (2022.7.1)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil<3,>=2.7.3->streamlit) (1.16.0)\n",
            "Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.18->streamlit) (1.26.16)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.18->streamlit) (2023.7.22)\n",
            "Requirement already satisfied: charset-normalizer~=2.0.0 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.18->streamlit) (2.0.12)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests<3,>=2.18->streamlit) (3.4)\n",
            "Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (3.0.0)\n",
            "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.10/dist-packages (from rich<14,>=10.14.0->streamlit) (2.14.0)\n",
            "Collecting pytz-deprecation-shim (from tzlocal<5,>=1.1->streamlit)\n",
            "  Downloading pytz_deprecation_shim-0.1.0.post0-py2.py3-none-any.whl (15 kB)\n",
            "Requirement already satisfied: decorator>=3.4.0 in /usr/local/lib/python3.10/dist-packages (from validators<1,>=0.2->streamlit) (4.4.2)\n",
            "Collecting smmap<6,>=3.0.1 (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit)\n",
            "  Downloading smmap-5.0.0-py3-none-any.whl (24 kB)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from jinja2->altair<6,>=4.0->streamlit) (2.1.3)\n",
            "Requirement already satisfied: attrs>=17.4.0 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (23.1.0)\n",
            "Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in /usr/local/lib/python3.10/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.19.3)\n",
            "Requirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.10/dist-packages (from markdown-it-py>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.2)\n",
            "Collecting tzdata (from pytz-deprecation-shim->tzlocal<5,>=1.1->streamlit)\n",
            "  Downloading tzdata-2023.3-py2.py3-none-any.whl (341 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m341.8/341.8 kB\u001b[0m \u001b[31m32.8 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hBuilding wheels for collected packages: validators\n",
            "  Building wheel for validators (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
            "  Created wheel for validators: filename=validators-0.20.0-py3-none-any.whl size=19580 sha256=49e0e7ff69aa75a0c90d709c9182b1771cd5ab6a57efa535b027e73a3368d636\n",
            "  Stored in directory: /root/.cache/pip/wheels/f2/ed/dd/d3a556ad245ef9dc570c6bcd2f22886d17b0b408dd3bbb9ac3\n",
            "Successfully built validators\n",
            "Installing collected packages: watchdog, validators, tzdata, smmap, pympler, pytz-deprecation-shim, pydeck, gitdb, tzlocal, gitpython, streamlit\n",
            "  Attempting uninstall: tzlocal\n",
            "    Found existing installation: tzlocal 5.0.1\n",
            "    Uninstalling tzlocal-5.0.1:\n",
            "      Successfully uninstalled tzlocal-5.0.1\n",
            "Successfully installed gitdb-4.0.10 gitpython-3.1.32 pydeck-0.8.0 pympler-1.0.1 pytz-deprecation-shim-0.1.0.post0 smmap-5.0.0 streamlit-1.25.0 tzdata-2023.3 tzlocal-4.3.1 validators-0.20.0 watchdog-3.0.0\n"
          ]
        }
      ]
    }
  ]
}