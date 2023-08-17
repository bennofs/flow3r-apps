from st3m.application import Application, ApplicationContext
from st3m.input import InputState
from ctx import Context
import st3m.run
from .VoIP import VoIPPhone, InvalidStateError

class App(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)

        phone=VoIPPhone("94.45.243.200", 5060, "8591", "cdwzNFQSc227", callCallback=self.answer, myIP="151.216.142.143")
        phone.start()

        # input('Press enter to disable the phone')
        # phone.stop()

    def answer(self, call): # This will be your callback function for when you receive a phone call.
        print("CALL")
        try:
            call.answer()

            call.hangup()
        except InvalidStateError:
            pass

    def draw(self, ctx: Context) -> None:
        pass
    
if __name__ == "__main__":
    # Continue to make runnable via mpremote run.
    st3m.run.run_view(App(ApplicationContext()))