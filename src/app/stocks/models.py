import datetime

class Stock(object):

    # Settings for calculating a recent price trend,
    # serves as basic check for a "reasonable" trend period
    # date change in DAYS, price change in PERCENTAGE
    local_extrema_min_date_change = 30
    local_extrema_max_date_change = 365*2
    local_extrema_min_price_change_pct = 0.20

    def get_latest_min_and_max_price_range(self, price_history):
        ''' Return the most recent price extremes (min, max) along
            with dates those prices occurred
            @param Dictionary price_history ie { '2014-01-01': 19.24, '2014-01-31':31.00 }
            @return Tuple (min_price_obj, max_price_obj)
                ie. ({'date':'2014-01-01', 'price':19.24}, {'date':'2014-01-31', 'price':31.00})
        '''
        min_price_obj = {'date':None, 'price':None}
        max_price_obj = {'date':None, 'price':None}

        dates = price_history.keys()
        dates.sort()
        dates.reverse()
        for date in dates:
            if min_price_obj['price'] is None or price_history[date] < min_price_obj['price']:
                min_price_obj['date'] = date
                min_price_obj['price'] = price_history[date]
            if max_price_obj['price'] is None or price_history[date] > max_price_obj['price']:
                max_price_obj['date'] = date
                max_price_obj['price'] = price_history[date]

            min_date = datetime.date(*[int(date_param) for date_param in min_price_obj['date'].split('-')])
            max_date = datetime.date(*[int(date_param) for date_param in max_price_obj['date'].split('-')])

            price_change_pct = (max_price_obj['price']-min_price_obj['price'])/((max_price_obj['price']+min_price_obj['price'])/2)
            if price_change_pct < self.local_extrema_min_price_change_pct:
                continue
            if abs((max_date-min_date).days) < self.local_extrema_min_date_change:
                continue
            elif abs((max_date-min_date).days) >= self.local_extrema_max_date_change:
                break

            # Once you continue backward in time to a 2nd price change over min threshold,
            # then you have found the 1st complete trend phase
            if min_price_obj['date'] < max_price_obj['date']:
                earlier_price = min_price_obj['price']
            else:
                earlier_price = max_price_obj['price']

            price_change_pct = (price_history[date]-earlier_price)/((price_history[date]+earlier_price)/2)
            if price_change_pct > self.local_extrema_min_price_change_pct:
                break

        return (min_price_obj, max_price_obj)

