# With terminal logging
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
)
    

# With file & terminal logging
# import logging
# import os

# def setup_logging():
#     os.makedirs("logs", exist_ok=True)

#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         handlers=[
#             logging.FileHandler("logs/app.log"),
#             logging.StreamHandler()  # still show in console
#         ]
#     )