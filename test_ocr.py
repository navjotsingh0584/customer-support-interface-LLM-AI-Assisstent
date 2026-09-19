from app.services.image_router import ImageRouter

router = ImageRouter()

result = router.process(
    r"C:\Users\HAL\Desktop\support_bot\app\uploads\143fbf4d-14fd-4f66-90f0-f61be4536711.jpg"
)

print("========== FINAL OUTPUT ==========")
print("SOURCE:", result["source"])
print("TYPE:", result["type"])
print(result["text"])
print("==================================")