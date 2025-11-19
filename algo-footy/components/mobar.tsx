"use client";
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { usePathname } from "next/navigation";

const navigation = [
    { name: 'Home', href: "/home", current: true },
    { name: 'Predictions', href: "/predictions", current: false },
    { name: 'Previous', href: "/previous", current: false }
]

function classNames(...classes: (string | undefined | null | false)[]) {
    return classes.filter(Boolean).join(' ')
}

export default function MobileNavBar() {
    const pathname = usePathname();
    return (
	<Disclosure as="nav"
	    className="lg:hidden relative bg-gradient-to-r from-[#001730] to-[#004080] dark:after:pointer-events-none dark:after:absolute dark:after:inset-x-0 dark:after:bottom-0 dark:after:h-px dark:after:bg-white/10"
	>
	     <div className="lg:hidden mx-auto max-w-7xl px-2 sm:px-6">
		 <div className="relative flex h-16 items-center justify-between">
		     <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
		         <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-white hover:text-orange-red focus:outline-2 focus:-outline-offset-1 focus:outline-indigo-500">
			     <span className="absolute -inset-0.5" />
			     <span className="sr-only">Menu</span>
		             <Bars3Icon aria-hidden="true" className="block size-6 group-data-open:hidden" />
                             <XMarkIcon aria-hidden="true" className="hidden size-6 group-data-open:block" />
			 </DisclosureButton>
		     </div>
		     <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
			 <div className="hidden sm:ml-6 sm:block">
                             <div className="flex space-x-4">
                                 {navigation.map((item) => {
				     const isActive = pathname.startsWith(item.href);
                                     return (
                                         <a
                                             key={item.name}
                                             href={item.href}
                                             aria-current={isActive ? 'page' : undefined}
                                             className={classNames(
                                                isActive
                                                    ? "lg:border-b-4 lg:border-orange-red font-bold text-orange-red"
                                                    : "border-b-0 border-orange-red",
                                                    'rounded-md px-3 py-2 text-sm font-medium',
                                             )}
                                         >
                                          {item.name}
                                        </a>
                                     );
                                   })}
                               </div>
			   </div>
                       </div> 
		  </div>
	     </div>
	     <DisclosurePanel className="sm:hidden lg:hidden">
                  <div className="space-y-1 px-2 pt-2 pb-3">
                      {navigation.map((item) => {
			  const isActive = pathname.startsWith(item.href);
			  return (
                              <DisclosureButton
                                  key={item.name}
                                  as="a"
                                  href={item.href}
                                  aria-current={isActive ? 'page' : undefined}
                                  className={classNames(
                                      isActive
                                          ? "lg:border-b-4 lg:border-orange-red font-bold text-orange-red"
                                      : "border-b-0 border-orange-red",
                                      'block rounded-md px-3 py-2 text-base font-medium',
                                  )}
                               >
                                   {item.name}
                             </DisclosureButton>
                         );
                       })}
                  </div>
             </DisclosurePanel>
	</Disclosure>
    )
}
