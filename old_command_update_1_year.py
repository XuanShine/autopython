schedule.cancel_job(jobs.get("update_price_wubook"))
jobs["update_price_wubook"] = schedule.every().hour.do(update_price_wubook(), 360)