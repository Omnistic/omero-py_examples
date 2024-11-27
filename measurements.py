import keyring as kr
import numpy as np
import pandas as pd
import omero2pandas

OMERO_HOSTNAME = 'EDIT_HERE'
OMERO_SERVICENAME = 'EDIT_HERE'

def connect_omero(username='EDIT_HERE'):
    connector = omero2pandas.OMEROConnection(server=OMERO_HOSTNAME, username=username, password=kr.get_password(OMERO_SERVICENAME,username),
                                             port=4064)
    connector.connect()
    return connector

def disconnect_omero(connector):
    connector.shutdown()

if __name__ == '__main__':
    col_names = ['Id', 'Mean', 'StdDev']
    dataset_id = 916
    img_ids = [12835, 12836, 12837]

    mean = []
    stddev = []

    conn = connect_omero()

    for img_id in img_ids:
        img = conn.get_gateway().getObject('Image', img_id)
        data = img.getPrimaryPixels().getPlane()

        mean.append(np.mean(data))
        stddev.append(np.std(data))

    img_ids = [str(img_id) for img_id in img_ids]
    img_ids.append('Average value')
    mean.append(np.mean(mean))
    stddev.append(np.mean(stddev))

    df = pd.DataFrame(list(zip(img_ids, mean, stddev)), columns=col_names)
    omero2pandas.upload_table(df, "Measurements", dataset_id, "Dataset", omero_connector=conn)

    disconnect_omero(conn)