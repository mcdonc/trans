/**
 * @author Mathias Teugels <mathias@tophima.com>
 * Copyright 2011 Tophima BVBA
 * All rights reserved
 */

/**
 * Requires:
 *  - jQuery
 */

var General = {
    update_timeout: 10 * 1000,
    
    init: function(e)
    {
        // Get all .toupdate elements
        $('.toupdate').live('change', General.update)
        
        if ($('.flashmessage').length > 0)
        {
            setTimeout('$(".flashmessage").remove()', 20 * 1000)
        }
    },
    
    update: function(e)
    {
        var $this = $(this)
        
        $this.siblings('.updatestatus').html('Updating...')
        
        $this.siblings('.updatestatus').each(function(i)
        {
            if (!$(this).hasClass('updating'))
            {
                $(this).addClass('updating')
            }
            
            if ($(this).hasClass('updated'))
            {
                $(this).removeClass('updated')
            }
            
            if ($(this).hasClass('updatefailed'))
            {
               $(this).removeClass('updatefailed')
            }
        })
        
        $.ajax({
            url: window.location + '/' + $this.attr('name') + '/',
            type: 'post',
            data: {'content': $this.val(), 'ajax_submitted': true},
            success: function(data, status, xhr)
            {
                $this.siblings('.updatestatus').html('Update succesful!')
                
                $this.siblings('.updatestatus').each(function(i)
                {
                    if ($(this).hasClass('updating'))
                    {
                        $(this).removeClass('updating')
                    }
                    
                    if (!$(this).hasClass('updated'))
                    {
                        $(this).addClass('updated')
                    }
                    
                    if ($(this).hasClass('updatefailed'))
                    {
                       $(this).removeClass('updatefailed')
                    }
                })
                
                setTimeout(General.removeUpdateStatus, General.update_timeout)
            },
            error: function(xhr, status, errorThrown)
            {
                $this.siblings('.updatestatus').html('Update failed!')
                
                $this.siblings('.updatestatus').each(function(i)
                {
                    if ($(this).hasClass('updating'))
                    {
                        $(this).removeClass('updating')
                    }
                    
                    if ($(this).hasClass('updated'))
                    {
                        $(this).removeClass('updated')
                    }
                    
                    if (!$(this).hasClass('updatefailed'))
                    {
                       $(this).addClass('updatefailed')
                    }
                })
            }
        })
    },
    
    removeUpdateStatus: function(e)
    {
        $('.updatestatus.updated').each(function(i)
        {
            $(this).removeClass('updated')
            $(this).html('')
        })
    }
}

$(document).ready(General.init)
