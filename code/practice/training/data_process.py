import numpy as np
from netCDF4 import Dataset

class Data_processing:
    def __init__(self,url):
        # 데이터를 가져오기 위한 url 저장
        self.url = url

        # 데이터셋 저장
        self.result = None
        self.pre_data = None

        # 시작, 끝 년도/월별 idx와 값 초기화
        self.start_y_idx = None
        self.end_y_idx = None
        self.end_month = None
        self.start_month = None

    def y_getter(self, variable):
        if variable == 'start':
            return self.start_y_idx
        else:
            return self.end_y_idx
        return 'input param like "start" or "end"'

    def m_getter(self, variable):
        if variable == 'start':
            return self.start_month
        else:
            return self.end_month
        return 'input param like "start" or "end"'

    # 데이터 전처리
    def get_data(self, variable, date=None):   # date는 년도, 월 순으로 기입 (예시 : 195001, 195001-198001)
        f = Dataset(self.url)
        f.set_auto_mask(False)
    
        result = f.variables[variable][:]
        result = result.reshape(-1,12,73,144)

    # 결측치 처리
        result = np.where(result==-9.99e+08, np.nan, result)

        if date is not None:
            # date가 범위인 경우 ('YYYY-YYYY') 처리 년도를 처리해줄 때 사용
            if '-' in date:
                start_date, end_date = date.split('-')
                start_year, self.start_month = int(start_date[:4]), int(start_date[4:])
                end_year, self.end_month = int(end_date[:4]), int(end_date[4:])

                # 날짜 범위에 맞는 인덱스를 찾아서 데이터 슬라이싱
                self.start_y_idx, self.end_y_idx = start_year - 1950, end_year - 1950  # 1950년을 기준으로 인덱스 계산

                # 날짜 범위에 맞게 데이터를 슬라이싱
                pre_data = result[self.start_y_idx:self.end_y_idx, :, :, :]
            
            else:
            # 단일 날짜에 대한 처리
                year, month = int(date[:4])-1950, 12 - int(date[4:])
                pre_data = result[year,month, :, :] # 해당 월에 해당하는 데이터 추출
            self.result, self.pre_data = result, pre_data 
        return result, pre_data

    # djf 월평균 데이터 출력
    def season_process(self, *seasons, anom_list=None):  # 입력: *seasons = ('djf1', 'djf2', 'mam', 'jja', 'son')
        data = self.pre_data if anom_list is None else anom_list
        print(data.shape)
        list_temp = []

        # 시즌별 데이터 처리 함수
        def process(season):
            """ 시즌에 맞는 처리 """
            if season == 'djf1':
                nino = np.concatenate([data[:-1], data[1:]], axis=1)
                return np.mean(nino[:, 11:14], axis=1)
            elif season == 'djf2':
                data_add = self.result[self.end_y_idx+1,:,:,:]
                
                # 만약 아노말리 리스트를 받은게 아니라면 실행 (데이터 맞추기기)
                if not np.array_equal(data, self.pre_data):
                    # 아노말리 구하기
                    climatology = np.nanmean(data_add, axis=0) 
                    anom = data_add - climatology 
                data_added = np.concatenate([data, anom[np.newaxis,:,:,:]], axis=0)
                data_added = data_added[1:,:,:,:]
                nino = np.concatenate([data_added[:-1], data_added[1:]], axis=1)
                return np.mean(nino[:, 11:14], axis=1)
            elif season == 'mam':       # [1:]
                print('functionnp.mean(data[:, 2:5], axis=1)', np.mean(data[:, 2:5], axis=1).shape)
                return np.mean(data[1:, 2:5], axis=1)  # MAM 처리
            elif season == 'jja':
                return np.mean(data[1:, 5:8], axis=1)  # JJA 처리
            elif season == 'son':
                return np.mean(data[1:, 8:11], axis=1)  # SON 처리
            return None

        # 매핑된 시즌들을 처리
        for season in seasons:
            season_data = process(season)
            # print(season_data, season)
            if season_data is not None:
                list_temp.append(season_data)

        return list_temp


    # nino 3.4 지역평균 데이터 출력
    def region_mean(self, data_list=None, nino34=False):
        # 위도 가중치 적용 (cos(lat))
        lat = np.arange(-90, 92.5, 2.5)  # 위도 배열 생성
        lat = np.cos(np.radians(lat))  # 위도에 따른 가중치 계산
        lat = np.full_like(data_list, lat[np.newaxis, :, np.newaxis])  # (29, 73, 144) 형태로 확장
        lat = np.where(np.isnan(data_list), np.nan, lat)  # 결측값 반영
        
        if nino34 is True:
            pick_dat = data_list[:,34:39, 76:97]
            pick_lat = lat[:,34:39, 76:97]
            idx = np.nansum(pick_dat * pick_lat, axis=(1, 2)) / np.nansum(lat, axis=(1, 2))  # (29,)
        # 위도 가중 평균 계산
        else:
            idx = np.nansum(data_list * lat, axis=(1, 2)) / np.nansum(lat, axis=(1, 2))  # (29,)

        return idx
        