import sys

import json
from datetime import datetime


import arrow

class Process:
	
	userD={}
	configD={}
	
	
	def __init__(self):
		global userD, configD
		
		userD=self.get_dict('user_ip.json')
		configD=self.get_dict('config.json')
		
	def main(self):		
		if len(sys.argv) != 2:
			raise Exception("File path not entered")
		else:
			filename=sys.argv[1]
			with open(filename,'r') as f:                
				lines=f.readlines()
				o=Process()
				for l in lines:  
					#print(f'processing: {l}')
					o.process_commands(l)
		
	
	def process_commands(self,user_ip):
		'''takes a single command(a line). sends to appropriate function'''
		
		global configD
				
		li=user_ip.split()
		for item in li:      
			#print(f'processing: {user_ip}')
			if item in configD['commands']:
				if item=='ADD_SUBSCRIPTION':
					r_add_sub=self.add_subscription(li)					
					if type(r_add_sub)!=int:
						print(f'{r_add_sub}')
					
				elif item=='ADD_TOPUP':
					if self.add_topup(li)!=1:
						print(self.add_topup(li))
					
				elif item=='START_SUBSCRIPTION':
					r_start_subs=self.start_subs(li)
					if not isinstance(r_start_subs, int):
						print(r_start_subs)
					
				elif item=='PRINT_RENEWAL_DETAILS':
					self.print_renewal()					
				break
	
	def start_subs(self,li):        
		global userD, configD

		ip_date=li[1]        
		fmt = "%d-%m-%Y"
		if userD['start_date']=='':
			try:
				if bool(datetime.strptime(ip_date, fmt)):
					userD['start_date']=ip_date
					return 1
				else:
					return "INVALID_DATE"
			except Exception:
				return "INVALID_DATE "
		else:
			return 0
		
		
		
		
	def add_subscription(self,li):        
		'''comm: ADD_SUBSCRIPTION. 
		argkey: list of user input'''
		
		global userD, configD
		
		s_category=li[1]
		p_name=li[2]          
		categ_plans=list(userD['categ_plan'].keys())    
		r=0  		
		if userD['start_date']!='':			
			if categ_plans[0]=='':   				
				if p_name in configD['PLAN_NAME'] and s_category in configD['SUBSCRIPTION_CATEGORY'] : 					
					userD['categ_plan']={s_category:p_name}
					return 1					
				else:
					r= 0
													
			elif s_category in categ_plans:
				return ('ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY')             
			
			elif p_name in configD['PLAN_NAME'] and s_category in configD['SUBSCRIPTION_CATEGORY'] :                      					
					d_=userD['categ_plan']
					d_.update({s_category:p_name})
					userD['categ_plan']=d_
					return 1
			r= 0
		else:
			r= 0			
		return r
	
	
	
	def add_topup(self,li):
		'''adds topup to userD '''
		
		global configD, userD
		categ_keys=list(userD['categ_plan'].keys())
		if categ_keys[0]!='':         
			t_name=li[1]
			t_months=li[2]
			topup_vals=list(userD['topup'].keys())
			if t_name in configD['ADD_TOPUP'] and t_months.isnumeric():
				
				if topup_vals[0]=='':
					userD['topup']={t_name:t_months}
					return 1
						
				else:
					return 'ADD_TOPUP_FAILED DUPLICATE_TOPUP'
			else:
				return 1
			
		else:
			return "ADD_TOPUP_FAILED SUBSCRIPTIONS_NOT_FOUND"
		
		
			
	def get_dict(self,json_file):
		''' takes json, returns dict'''
		with open(json_file,"r") as file:
			jsonD = json.load(file)
			return jsonD


	def calculate(self):
		'''calculates renewal date and renewal cost'''
		global userD, configD
		fmt = "%d-%m-%Y"
		ret_str=''
		s=0
		
		if userD['start_date']=='':
			return "SUBSCRIPTIONS_NOT_FOUND"
		#rules        
		prices=configD['prices']
			   
		# expect d: {'MUSIC': 'PERSONAL', 'VIDEO': 'PREMIUM', 'PODCAST': 'FREE'}
		d=userD['categ_plan']        
		for plan_name, tier in d.items():
			
			li=prices[plan_name]                        
			for t in li:
				for k, v in t.items():
					if k == tier:
					
						for k_, v_ in v.items():
							months_=int(k_)
							price_=int(v_)
							s+=price_
							
							ip_date=userD['start_date']
							
							o=arrow.get(ip_date,'DD-MM-YYYY')
							o=o.shift(months=months_)
							o=o.shift(days=-10)                      
							str_d=o.format(fmt)
							ret_str +=f"RENEWAL_REMINDER {plan_name} {str_d}\n"

		d=userD['topup']
		for device_c, no_of_device in d.items():
		   
			if device_c=='FOUR_DEVICE':
				s+=50*int(no_of_device)
			elif device_c=='TEN_DEVICE':
				s+=100*int(no_of_device)
				
		ret_str +=f'RENEWAL_AMOUNT {s}'
		
		return ret_str


	def print_renewal(self):
		global userD
				
		if userD['start_date']=='':
			print("SUBSCRIPTIONS_NOT_FOUND")
		else:
			categ_plans=list(userD['categ_plan'].keys())
			if categ_plans[0]=='':   
				print("SUBSCRIPTIONS_NOT_FOUND")
			else:
				print(self.calculate())  

if __name__ == "__main__":
	o=Process()
	o.main()
