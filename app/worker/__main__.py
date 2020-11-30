import app.worker as worker

worker.set_faust_app_for_worker()

faust_app = worker.get_faust_app()

faust_app.main()
