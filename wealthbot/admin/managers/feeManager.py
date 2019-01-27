from django.core.exceptions import PermissionDenied
from admin.models import Fee

class FeeManager(object):

	# Return ria related system fees.
	def getAdminFee(self, ria):
		billingSpec = ria.appointedBillingSpec

		if billingSpec is None:
			return []

		if billingSpec.owner != None:
			raise PermissionDenied('Owner of Admin Billing Spec for RIA must be null. May be it is not admin fees?')

		return billingSpec.fees.all()

	# Get client's fee structure.
	def getClientFees(self, ria, riaFees=None):
		adminFees = self.getAdminFee(ria=ria)

		sortFees = []
		for adminFee in adminFees:
			sortFees.append(adminFee.tier_top)

		# Add to array all fees from ria
		if riaFees is not None:
			for riaFee in riaFees:
				if isinstance(riaFee, Fee):
					if (riaFee.tier_top is not None) and (riaFee.tier_top not in sortFees):
						sortFees.append(riaFee.tier_top)
				else:
					if ('tier_top' in riaFee):
						if riaFee['tier_top'] not in sortFees:
							sortFees.append(riaFee['tier_top'])
		sortFees.sort()

		# Search intervals and calculate total fees for client
		start = 0
		currFeeWithoutRetirement = 0
		currFeeWithRetirement = 0
		clientFees = []

		for sortFee in sortFees:
			# Search admin fee
			for adminFee in adminFees:
				if adminFee.tier_top >= sortFee:
					currFeeWithoutRetirement = adminFee.fee_without_retirement
					currFeeWithRetirement = adminFee.fee_with_retirement
					break

			# Search client fee
			for riaFee in riaFees:
				if isinstance(riaFee, Fee):
					if riaFee.tier_top >= sortFee:
						currFeeWithoutRetirement += riaFee.fee_without_retirement
						currFeeWithRetirement += riaFee.fee_with_retirement
						break
				else:
					if 'tier_top' in riaFee:
						if riaFee['tier_top'] >= sortFee:
							currFeeWithoutRetirement += riaFee['fee_without_retirement']
							currFeeWithRetirement += riaFee['fee_without_retirement']
							break

			# Store data
			currFeeCard['tier_bottom'] = start
			currFeeCard['tier_top'] = sortFee
			currFeeCard['fee_without_retirement'] = currFeeWithoutRetirement
			start = sortFee + 0.01
			clientFees.append(currFeeCard)

		return clientFees
