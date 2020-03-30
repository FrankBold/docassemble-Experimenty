import stripe
import json
from docassemble.base.util import word, get_config, action_argument, DAObject, prevent_going_back
from docassemble.base.standardformatter import BUTTON_STYLE, BUTTON_CLASS

stripe.api_key = get_config('stripe secret key')

__all__ = ['DAStripe']

class DAStripe(DAObject):
  def init(self, *pargs, **kwargs):
    if get_config('stripe public key') is None or get_config('stripe secret key') is None:
      raise Exception("In order to use a DAStripe object, you need to set stripe public key and stripe secret key in your Configuration.")
    super().init(*pargs, **kwargs)
    if not hasattr(self, 'button_label'):
      self.button_label = "Zaplatit"
    if not hasattr(self, 'button_color'):
      self.button_color = "primary"
    if not hasattr(self, 'error_message'):
      self.error_message = "Zkuste prosím jiný způsob platby."
    self.is_setup = False

  def setup(self):
    float(self.amount)
    str(self.currency)
    self.intent = stripe.PaymentIntent.create(
      amount=int(float('%.2f' % self.amount)*100.0),
      currency=self.currency,
    )
    self.is_setup = True

  @property
  def html(self):
    if not self.is_setup:
      self.setup()
    return """\
<label for="stripe-card-element" class="col-md-4 col-form-label da-form-label datext-right">Platební údaje</label>
<div id="stripe-card-element" class="mt-2"></div>
<div id="stripe-card-errors" class="mt-2 mb-2 text-alert" role="alert"></div>
<button class="btn """ + BUTTON_STYLE + self.button_color + " " + BUTTON_CLASS + '"' + """ id="stripe-submit">""" + word(self.button_label) + """</button>"""

  @property
  def javascript(self):
    if not self.is_setup:
      self.setup()
    billing_details = dict()
    try:
      billing_details['name'] = str(self.payor)
    except:
      pass
    address = dict()
    try:
      address['postal_code'] = self.payor.billing_address.zip
    except:
      pass
    try:
      address['line1'] = self.payor.billing_address.address
      address['line2'] = self.payor.billing_address.formatted_unit()
      address['city'] = self.payor.billing_address.city
      if hasattr(self.payor.billing_address, 'country'):
        address['country'] = address.billing_country
      else:
        address['country'] = 'CZ'
    except:
      pass
    if len(address):
      billing_details['address'] = address
    try:
      billing_details['email'] = self.payor.email
    except:
      pass
    try:
      billing_details['phone'] = self.payor.phone_number
    except:
      pass
    return """\
<script>
  var stripe = Stripe(""" + json.dumps(get_config('stripe public key')) + """);
  var elements = stripe.elements();
  var elementStyles = {
    base: {
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
      fontSize: '1rem',
      fontWeight: '400',
      lineHeight: '1.5',
      color: '#5a5a5a',
      backgroundColor: '#222',
      
      '::placeholder': {
        color: '#888',
      },
      ':-webkit-autofill': {
        color: '#e39f48',
      },
    },
    invalid: {
      color: '#E25950',

      '::placeholder': {
        color: '#FFCCA5',
      },
    },
  };
  var card = elements.create("card", { style: elementStyles });
  card.mount("#stripe-card-element");

  card.addEventListener('change', ({error}) => {
    const displayError = document.getElementById('stripe-card-errors');
    if (error) {
      displayError.textContent = error.message;
    } else {
      displayError.textContent = '';
    }
  });
  var submitButton = document.getElementById('stripe-submit');
  submitButton.addEventListener('click', function(ev) {
    stripe.confirmCardPayment(""" + json.dumps(self.intent.client_secret) + """, {
      payment_method: {
        card: card,
        billing_details: """ + json.dumps(billing_details) + """
      }
    }).then(function(result) {
      if (result.error) {
        flash(result.error.message + "  " + """ + json.dumps(word(self.error_message)) + """, "danger");
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          action_perform(""" + json.dumps(self.instanceName + '.success') + """, {result: result})
        }
      }
    });
  });
</script>
    """
  @property
  def paid(self):
    if not self.is_setup:
      self.setup()
    if hasattr(self, "payment_successful") and self.payment_successful:
      return True
    if not hasattr(self, 'result'):
      self.demand
    payment_status = stripe.PaymentIntent.retrieve(self.intent.id)
    if payment_status.amount_received == self.intent.amount:
      self.payment_successful = True
      return True
    return False
  def process(self):
    self.result = action_argument('result')
    self.paid
    prevent_going_back()