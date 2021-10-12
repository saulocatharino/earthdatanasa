#  Earth Data Nasa Imagery 
Get satellites images at realtime and detect clouds from Nasa Data using Python/Streamlit and RestAPI.<br><br>
Requirements:<br>
Opencv, Numpy & Streamlit<br>
<br>
To install dependencies:<br>
pip3 install opencv-python<br>
pip3 install numpy<br>
pip3 install streamlit<br>
<br><br>
To execute:
<br>
<br>streamlit run app.py
<br>
<br>
# How it Works?
Inside script 'utils.py' have two functions: 'convert' and 'get'.<br>
<br>
The function 'convert' converts from latitude and longitude to epsg4326 projection.
<br>
The function 'get' request a image using RestAPI with especified parameters.
# Citing

If you use our code,please cite our work

@misc{saulocatharino,
     title={Earth-Data-Nasa-Imagery}, 
     author={Saulo Catharino},
     year={2021},
     email={saulocatharino@gmail.com}
}
