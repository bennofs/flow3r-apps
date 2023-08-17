from st3m.application import Application, ApplicationContext
from st3m.input import InputState
from ctx import Context
import st3m.run
import network

#PROFILES = ['open', 'enterprise'] enterprise doesn't really work
PROFILES = ['open']

class App(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.wlan = network.WLAN(network.STA_IF)
        self.status = None
        self.update_status()
        self.cert = None
        self.current_profile = 0

    def update_status(self):
        if not self.wlan.active():
            self.status = None
            return

        if self.wlan.isconnected():
            self.status = self.wlan.ifconfig()[0]
        elif self.wlan.active() and self.wlan.status() == 1001:
            self.status = 'connecting'
        else:
            self.status = None

    def connect_camp_open(self):
        self.wlan.active(True)
        self.wlan.connect('Camp2023-open')

    def connect_camp_ent(self):
        if not self.cert:
            with open('/flash/sys/apps/wifi/ca.pem', 'rb') as f:
                self.cert = f.read()
        self.wlan.active(True)
        self.wlan.connect('Camp2023-open', ent_username='camp', ent_password='camp', ent_ca_cert=self.cert)

    def disconnect(self):
        self.wlan.disconnect()
        self.wlan.active(False)

    def draw(self, ctx: Context) -> None:
        # Paint the background black
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        if self.status == 'connecting':
            ctx.rgb(255, 255, 255)
            ctx.move_to(-95, -40)
            ctx.font = "Camp Font 1"
            ctx.text(self.status)
            ctx.rgb(255, 255, 0).round_rectangle(-20,-20, 40, 40, 40).fill()
        elif self.status:
            ctx.rgb(255, 255, 255)
            ctx.move_to(-90, -45)
            ctx.font = "Camp Font 1"
            ctx.text(self.status)
            ctx.rgb(0, 255, 0).round_rectangle(-30,-30, 60, 60, 60).fill()
        else:
            ctx.rgb(255, 255, 255)
            ctx.move_to(-65, -50)
            ctx.font = "Camp Font 1"
            ctx.text("WIFI - OFF")
            ctx.rgb(255, 0, 0).round_rectangle(-30,-30, 60, 60, 60).fill()

        ctx.move_to(-35, 60)
        ctx.font = 'Camp Font 2'
        ctx.text('profile')
        ctx.move_to(-45, 85)
        profile = PROFILES[self.current_profile]
        pad = (max(0, 12 - len(profile)) // 2) * " "
        ctx.text(pad + profile)

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms)
        if self.input.buttons.app.middle.pressed:
            if self.status:
                self.disconnect()
            else:
                if PROFILES[self.current_profile] == 'open':
                    self.connect_camp_open()
                elif PROFILES[self.current_profile] == 'enterprise':
                    self.connect_camp_ent()

        if self.input.buttons.app.left.pressed and not self.status:
            self.current_profile = (self.current_profile - 1) % len(PROFILES)

        if self.input.buttons.app.right.pressed and not self.status:
            self.current_profile = (self.current_profile + 1) % len(PROFILES)

        self.update_status()

if __name__ == '__main__':
    # Continue to make runnable via mpremote run.
    st3m.run.run_view(App(ApplicationContext()))
