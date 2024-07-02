from fastapi import FastAPI
places = { 'delhi': ['Red Fort', 'Qutub Minar', 'India Gate'],
                   'mumbai': ['Gateway of India', 'Marine Drive', 'Elephanta Caves'],
                   'jaipur': ['Hawa Mahal', 'Amber Fort', 'City Palace'],
                   'varanasi': ['Kashi Vishwanath Temple', 'Ghats of Ganges', 'Sarnath'],
                   'goa': ['Baga Beach', 'Calangute Beach', 'Dudhsagar Falls']}
app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/places/{city}")
async def get_places(city: str):
    return places[city]