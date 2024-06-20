from app.views import app_views
from app.models.order import Order
from app.models.review import Review
from flask import request, abort
from app.models import db

@app_views.route('/order/<order_id>/review', methods=["POST"])
def post_review(order_id=None):

    order = Order.query.filter_by(id=order_id).one_or_404()

    rating = request.form.get('rating')
    review = request.form.get('review')

    if not (review and rating):
        abort(404)

    new_review = Review(order_id = order.id, product_id=order.product.id,
                        rating=rating, review=review)
    db.session.add(new_review)
    db.session.commit()

    # review = Review()
    return """
         <div class='font-roboto flex py-3 flex-col justify-center items-center gap-3'>
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" width="84" height="84" viewBox="0 0 84 84" fill="none">
                    <path opacity="0.5" d="M84 42C84 65.1958 65.1958 84 42 84C18.804 84 0 65.1958 0 42C0 18.804 18.804 0 42 0C65.1958 0 84 18.804 84 42Z" fill="#03CB2F" fill-opacity="0.15"/>
                    <path d="M58.9276 29.2727C60.1578 30.5028 60.1578 32.4973 58.9276 33.7273L37.9276 54.7273C36.6975 55.9575 34.7033 55.9575 33.473 54.7273L25.073 46.3273C23.8429 45.0972 23.8429 43.103 25.073 41.8728C26.3031 40.6426 28.2976 40.6426 29.5278 41.8728L35.7004 48.0451L45.0865 38.659L54.4731 29.2727C55.7033 28.0426 57.6975 28.0426 58.9276 29.2727Z" fill="#03CB2F"/>
                </svg>
            
            </span>

            <p class='text-xs text-center text-sc-gray-dark'> Thank you! Your review has been successfully submitted. We appreciate your feedback</p>

            <button
                type="button"
                aria-controls="drawer-bottom-example"
                data-drawer-hide="leave-review"
                class="text-pc-teal-normal font-roboto tracking-widest text-sm  bg-sc-gray-light   focus:outline-none w-full dark:focus:ring-teal-800 font-medium rounded-lg px-6 py-2.5 text-center">Go back
            </button>

        </div>
    """


