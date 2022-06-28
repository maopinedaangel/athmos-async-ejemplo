from datetime import datetime, timedelta
import time
import uuid
import random
#Importar la librería asyncio para usar programación concurrente
import asyncio


class OrdersManager:
    __orders = []
    __orders_processed = 0
    __last_printed_log = datetime.now()

    def __init__(self) -> None:
        self.__generate_fake_orders(quantity=1_000)

    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        self.__orders = [(uuid.uuid4(), x) for x in range(quantity)]
        self.__log(f"{len(self.__orders)} generated...")

    def __log(self, message):
        print(f"{datetime.now()} > {message}")

    #Al agregar la palabra reservada async, la función se convierte en una rutina (coroutine)
    async def __fake_save_on_db(self, order):
        id, number = order

        self.__log(
            message=f"Order [{id}] {number} was successfully prosecuted."
        )

        #
        await asyncio.sleep(random.uniform(0, 1))        

    #Función definida como rutina (coroutine)
    async def process_orders(self):
        #Definir una lista para almacenar las tareas
        coroutines = []        
        for order in self.__orders:
            #Generar una tarea por cada orden y guardarla en la lista de tareas
            coroutines.append(self.__fake_save_on_db(order=order))         
            self.__orders_processed += 1

            if datetime.now() > self.__last_printed_log:
                self.__last_printed_log = datetime.now() + timedelta(seconds=5)
                self.__log(
                    message=f"Total orders executed: {self.__orders_processed}/{len(self.__orders)}"
                )
        #Ejecutar todas las tareas. La palabra reservada await permite ceder la ejecución a otra tarea, cuando la presente se encuentra en espera.              
        res = await asyncio.gather(*coroutines)
        return res

    #Definir un nuevo método para que dirija el proceso completo
    def run_process(self):
        loop = asyncio.get_event_loop() 
        loop.run_until_complete(self.process_orders())
        loop.close()               
        

#
#
# ---
orders_manager = OrdersManager()

start_time = time.time()

#Ejecutar el proceso
orders_manager.run_process()

delay = time.time() - start_time

print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")
