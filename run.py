from app import app, db


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2025, debug=True)
