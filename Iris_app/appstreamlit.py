import streamlit as st

# first part
# streamlit - top javascript and html
'''
st.title("Streamlit Apps!")

st.header("This is a header")

st.subheader("This is a subheader")

st.text("This is a text")

st.write("This is a write")


# Use inline html
st.write('<p style="font-size:20px; color:red">This is the text</p>',
         unsafe_allow_html=True)

# multi line
st.write("""This is an example
of writting text
on multiple lines

""")

#markdown

#link
st.markdown("[link](https://www.markdownguide.org/cheat0sheet/)")

#emoji
st.markdown(":streamlit: :grimacing:")
'''

# html integration

st.markdown("### HTML")

html_code = """
<p style="font-size:20px; color:red">This is the text</p>
<h1 style="color:blue"> This is the text</h1>
"""

st.markdown(
"""
<style>
h1{
color:blue;
}
p{
color:red;
}

</style>

""",
unsafe_allow_html=True
)


#latex - formatting

st.latex("x^2 + y^2 = z^2")

name = st.text_input("Type here...")
feedback = st.text_area("Enter your feedback", "Type here....")

age = st.number_input("Enter your age", format="%d", value=12, min_value=12, max_value=120)

date = st.date_input("Enter yout date", format='YYYY/MM/DD')
time = st.time_input("Enter your time")

st.write("name", name)


button = st.button("Click Me")

if button:
    st.text("You have clicked me")


checkbox = st.checkbox('Check me to enable smtg')

if checkbox:
    st.write("You have checked me")

list1 = ["NLP","ML","DL","DS"]
radio_button = st.radio('Radio button', list1)
st.write(radio_button)


#selectbox = st.selectbox("Select an option", list*20)
#st.write(selectbox)

multiselectbox = st.multiselect("Select multiple option", list1, default="NLP")
st.write(multiselectbox[0])

rating = st.slider("select your rating", list1)
st.write(rating)

select_slider, select_slider2 = st.select_slider("select your rating", list1,
                                                 values=("NLP","DL"))
st.write(select_slider, select_slider2)