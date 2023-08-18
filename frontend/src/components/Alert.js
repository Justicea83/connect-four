import {CheckCircleIcon, XMarkIcon} from '@heroicons/react/20/solid'
import classNames from "@/utils/misc";
import PropTypes from "prop-types";

export default function Alert({message, type, close}) {
    return (
        <div className={classNames(
            "rounded-md p-4",
            type === 'success' && 'bg-green-50',
            type === 'error' && 'bg-red-50',
        )}>
            <div className="flex">
                {type === 'success' && <div className="flex-shrink-0">
                    <CheckCircleIcon className="h-5 w-5 text-green-400" aria-hidden="true"/>
                </div>}
                <div className="ml-3">
                    <h3 className={classNames(
                        'text-sm font-medium',
                        type === 'success' && 'text-green-800',
                        type === 'error' && 'text-red-700',
                    )}>{message}</h3>
                </div>
                <div className="ml-auto pl-3">
                    <div className="-mx-1.5 -my-1.5">
                        <button
                            type="button"
                            className={
                                classNames(
                                    "inline-flex rounded-md  p-1.5   focus:outline-none focus:ring-2  focus:ring-offset-2 ",
                                    type === 'success' && 'bg-green-50 text-green-500 hover:bg-green-100 focus:ring-green-600 focus:ring-offset-green-50',
                                    type === 'error' && 'bg-red-50 text-red-500 hover:bg-red-100 focus:ring-red-600 focus:ring-offset-red-50'
                                )
                            }
                        >
                            <span className="sr-only">Dismiss</span>
                            <XMarkIcon onClick={close} className="h-5 w-5" aria-hidden="true"/>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

Alert.propTypes = {
    message: PropTypes.string,
    type: PropTypes.oneOf(['success', 'error']),
    close: PropTypes.func
}