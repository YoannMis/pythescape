import castle

class App(castle.Rules):

    def start_app(self):
        self()()

if __name__ == '__main__':
    app = App()
    app.start_app()
